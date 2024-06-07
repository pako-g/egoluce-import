import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

TIPO = 'Lampade a Sospensione'
BRAND ='Egoluce'

urlsCategory = []
urlsProduct = []
names = {}

colors = {'00': 'Trasparente', '01': 'Bianco', '02': 'Nero', '03': 'Grigio', '05': 'Rosso', '06': 'Verde',
          '08': 'Giallo', '09': 'Arancione', '10': 'Azzurro', '11': 'Rosa', '14': 'Lavagna', '23': 'Alluminio Satinato',
          '24': 'Cromo Nero', '25': 'Dorato Satinato', '28': 'Foglia Rame', '29': 'Foglia Oro', '30': 'Foglia Argento',
          '31': 'Cromato', '32': 'Nickel Satinato', '33': 'Acciaio Satinato', '34': 'Verniciato Corten',
          '35': 'Verniciato Sabbia', '21': 'Dorato Lucido', '38': 'Ramato Lucido', '39': 'Verniciato Antracite',
          '45': 'Allumino Anodizzato', '50': 'Cristallo', '56': 'Specchio', '57': 'Vetro Bianco',
          '85': 'Verniciato Argento', '86': 'Verniciato Oro', '87': 'Verniciato Rame', '88': 'Verniciato Bronzo',
          '70': 'Retrò', '71': 'Fumè'}

tempColor = {'XW': '2700K', 'WW': '3000K', 'W': '4000k', 'CW': '5000k'}
dimmerEmerg = {'EM': 'Lampada di Emergenza', 'DIM': 'Dimmer Push', 'DALI': 'Dimmer Dali'}
otherConf = {'IP': 'IP44', 'P': 'IP44', 'ST': 'Diffusore Satinato', 'TR': 'Diffusore Trasparente'}
ottica = {'25': 'Apertura Ottica 25°', '48': 'Apertura Ottica 48°', '63': 'Apertura Ottica 63°', 'ST': 'Vetro Satinato'}

def getAllCategoryUrls(links):
    for link in links.find_all('a'):
        urlsCategory.append(link['href'])


def getRequest(url):
    reqs = requests.get(url)
    content = reqs.text
    return BeautifulSoup(content, 'html.parser')


def createTittle(tag):
    name = tag.find('')
    #print('Egoluce ' + i.find('h4').text)


def main():
    df = pd.read_csv('egoluce-2023.csv')
    soup = getRequest('https://egoluce.com/')

    link_menu = soup.find('li', class_='wells liindice')

    getAllCategoryUrls(link_menu)

    #print(urlsCategory)
    #analyzeSku(df)


    for url in urlsCategory:
        #print(url)
        #CAMBIARE PER TIPOLOGIA
        if url == 'https://egoluce.com/'+'tipologia-sospensioni.html':
            soup = getRequest(url)
            link_lamps = soup.findAll('a', class_='bradius')


            for lamp in link_lamps:
                soup = getRequest('https://egoluce.com/' + lamp['href'])

                col = soup.find('div', class_='container').findAll('div', class_='col-sm-4')

                #dimensioni = {}

                for i in col:
                    #print(i)
                    #print(i.find('h4').text)
                    #print(i.find('h5').text)
                    #print((i.find('h5').find_next_siblings('h5')[0]))
                    #tmp = i.find('h5').find_next_siblings('h5')[0]
                    #print(i.find('small').text)
                    #names[i.find('h4').text] = i.find('h5').text
                    # CAMBIARE PER TIPOLOGIA
                    if i.find('small').text == 'sospensioni':
                        urlsProduct.append('https://egoluce.com/' + i.find('a', class_='aa')['href'])

                    #print('https://egoluce.com/' + i.find('a', class_='aa')['href'])
                    #soup = getRequest('https://egoluce.com/' + i.find('a', class_='aa')['href'])
                    # singleImageUrl = soup.find('div', class_='container').find('a', class_='fancybox')
                    # galleryUrls = soup.find('div', class_='container').findAll('a', class_='fancybox')
                    #allImg = soup.findAll('a', class_='fancybox')
                    #print(allImg)

                    #dimensioni[i.find('h4').text] = i.find('h5').find_next_siblings('h5')[0].text

                #print(urlsProduct)
                #print(dimensioni)
                product_list_final = []
                for url in urlsProduct:
                    #print(url)

                    sku = url[url.index("uid"):][4:]
                    name = (url[url.index("nf"):])
                    name = name[:name.index('&')][3:]
                    #print(name)
                    #print(sku)

                    result = df[df['Articolo'].str.contains(sku)]

                        #print('Number :', index)
                    product_list_final = createSingleProducts(result,name,sku)
                    print(product_list_final)


                break



def createSingleProducts(result, name, sku):
    simpleProducts = []
    for index, row in result.iterrows():
        simple_product = {}
        color = getColor(row.get('Articolo'))
        temperaturaColore = getTempColor(row.get('Articolo'))

        simple_product['sku'] = 'EG-' + row.get('Articolo')
        title = BRAND + ' ' + name.capitalize()

        if color != '':
            title += ' ' + color
            simple_product['color'] = color

        if temperaturaColore != '':
            title += ' ' + temperaturaColore
            simple_product['config_temperatura_colore'] = temperaturaColore

        title += ' ' + TIPO + ' ' + row.get('Articolo')
        simple_product['name'] = title
        simple_product['price'] = row.get('Prezzo')
        simple_product['product_type'] = 'simple'
        simple_product['visibility'] = 'Not Visible Individually'

        #print(simple_product)
        simpleProducts.append(simple_product)

    return simpleProducts


def getColor(sku):
    if sku.find('.') > -1:
        sku = sku[sku.find('.'):][1:]
        if sku.find('/') > -1:
            sku = sku[:sku.find('/')]
        #print(sku)
        if sku.find('.') > -1:
            #print(sku[0:2])
            #print(sku[3:5])
            #print(colors[sku[0:2]])
            #print(colors[sku[3:5]])
            return colors[sku[0:2]] + ' / ' + colors[sku[3:5]]
        else:
            return colors[sku]
    else:
        return ''

def getTempColor(sku):
    for t in tempColor:
        if sku.find(t) > -1:
            return tempColor[t]
    return ''


def analyzeSku(df):
    for index, row in df.iterrows():
        #print('Number :', index)
        #print(row.get('Articolo'))
        sku = row.get('Articolo')
        split = re.split(r"[./\s]\s*", sku)
        print(split)



if __name__ == '__main__':
    main()