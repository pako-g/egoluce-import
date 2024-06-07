import os.path
import string
import requests
from bs4 import BeautifulSoup
import re
import validators
from validators import ValidationFailure

urlsCategory = []
urlsProduct = []

colors = {'00': 'Trasparente', '01': 'Bianco', '02': 'Nero', '03': 'Grigio', '05': 'Rosso', '06': 'Verde',
          '08': 'Giallo', '09': 'Arancione', '10': 'Azzurro', '11': 'Rosa', '14': 'Lavagna', '23': 'Alluminio Satinato',
          '24': 'Cromo Nero', '25': 'Dorato Satinato', '28': 'Foglia Rame', '29': 'Foglia Oro', '30': 'Foglia Argento',
          '31': 'Cromato', '32': 'Nickel Satinato', '33': 'Acciaio Satinato', '34': 'Verniciato Corten',
          '35': 'Verniciato Sabbia', '21': 'Dorato Lucido', '38': 'Ramato Lucido', '39': 'Verniciato Antracite',
          '45': 'Allumino Anodizzato', '50': 'Cristallo', '56': 'Specchio', '57': 'Vetro Bianco',
          '85': 'Verniciato Argento', '86': 'Verniciato Oro', '87': 'Verniciato Rame', '88': 'Verniciato Bronzo'}

tempColor = {'XW': '2700K', 'ww': '3000K', 'W': '4000k', 'CW': '5000k'}

otherSym = {'ST': 'Diffusore Satinato', 'TR': 'Diffusore Trasparente', 'EM': 'Lampada di Emergenza',
            'DIM': 'Dimmer Push', 'DALI': 'Dimmer Dali'}

ROOT = 'Egoluce'
RESIZE = 'resize'
SCORE = '-'

def getAllCategoryUrls(links):
    for link in links.find_all('a'):
        urlsCategory.append(link['href'])


def getRequest(url):
    reqs = requests.get(url)
    content = reqs.text
    return BeautifulSoup(content, 'html.parser')

def replace_name(string):
    string = re.sub("[?]", '', string)
    string = re.sub("[,]", '-', string)
    string = re.sub("[.!]", "-", string)
    string = re.sub("[ /]", "-", string)
    string = re.sub("è", "e", string)
    string = re.sub("--", "", string)
    string = re.sub("'", "", string)
    return string


def createName(tag, category):
    cat = ''
    if category.find('sospensioni') != -1:
        cat = 'lampada-a-sospensione'
    if category.find('tavolo') != -1:
        cat = 'lampada-da-tavolo'
    if category.find('terra') != -1:
        cat = 'lampada-da-terra'
    if category.find('parete') != -1:
        cat = 'lampada-da-parete'
    if category.find('plafone') != -1:
        cat = 'lampada-da-soffitto'
    if category.find('parete%20plafone') != -1:
        cat = 'lampada-da-parete'
    if category.find('incasso') != -1:
        cat = 'lampada-da-incasso'
    if category.find('sistemi%20di%20luce') != -1:
        cat = 'sistemi'
    if category.find('da%20esterno') != -1:
        cat = 'lampada-da-esterno'
    if category.find('proiettori') != -1:
        cat = 'proiettori'

    sku = tag.find('h4').text.strip()
    name = replace_name(str.lower(tag.find('h5').text.strip()))
    return 'egoluce-'+name+'-'+cat+'-'+sku




def main():

    if not os.path.isdir(os.path.join(os.getcwd(), ROOT)):
        os.mkdir(os.path.join(os.getcwd(), ROOT))


    soup = getRequest('https://egoluce.com/')

    link_menu = soup.find('li', class_='wells liindice')

    getAllCategoryUrls(link_menu)

    #print(urlsCategory)

    for url in urlsCategory:
        soup = getRequest(url)
        link_lamps = soup.findAll('a', class_='bradius')
        #print(link_lamps)
        print(url)

        for lamp in link_lamps:
            soup = getRequest('https://egoluce.com/' + lamp['href'])

            col = soup.find('div', class_='container').findAll('div', class_='col-sm-4')
            for i in col:
                name = createName(i, url)
                print(name)
                subdirectory = os.path.join(os.getcwd() + '/' + ROOT,
                                            replace_name(str.lower(i.find('h5').text.strip())).capitalize()
                                            + '-' + i.find('h4').text.strip())
                if not os.path.isdir(subdirectory):
                    os.mkdir(subdirectory)
                    os.mkdir(os.path.join(subdirectory, RESIZE))

                print(subdirectory)
                print('----------------------------')

                urlsProduct.append('https://egoluce.com/' + i.find('a', class_='aa')['href'])
                #print('https://egoluce.com/' + i.find('a', class_='aa')['href'])
                soup = getRequest('https://egoluce.com/' + i.find('a', class_='aa')['href'])
                # singleImageUrl = soup.find('div', class_='container').find('a', class_='fancybox')
                # galleryUrls = soup.find('div', class_='container').findAll('a', class_='fancybox')
                allImg = soup.findAll('a', class_='fancybox')
                j = 0
                for img in allImg:
                    j += 1
                    print(img['href'])
                    print(len(allImg))
                    if j == 1:
                        download_image(os.path.join(subdirectory, name+'.jpg'), 'https://egoluce.com/'+img['href'])
                    if j == len(allImg):
                        download_image(os.path.join(subdirectory, name + '-dimensioni' + '.jpg'), 'https://egoluce.com/' + img['href'])
                    if j != len(allImg) and j != 1:
                        download_image(os.path.join(subdirectory, name+'-'+str(j)+'.jpg'), 'https://egoluce.com/'+img['href'])

            #break

        break



def download_image(name, url):
    #print(name)
    #print(url)
    if isinstance(validators.url(str(url)), ValidationFailure):
        return

    # Define HTTP Headers
    headers = {"User-Agent": "Chrome/106.0.5249.119"}
    # Send GET request
    response = requests.get(url, headers=headers)
    # Save the image
    if response.status_code == 200:
        with open(name, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)

    #time.sleep(2.5)









if __name__ == '__main__':
    main()