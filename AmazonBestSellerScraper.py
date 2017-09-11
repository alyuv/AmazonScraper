import time
import sys
import re
import requests
from bs4 import BeautifulSoup

urls=[
    'http://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Automotive/zgbs/automotive/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Beauty/zgbs/beauty/ref=zg_bs_nav_0',
    'http://www.amazon.com/best-sellers-camera-photo/zgbs/photo/ref=zg_bs_nav_0'
    'http://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Clothing/zgbs/apparel/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Computers-Accessories/zgbs/pc/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Health-Personal-Care/zgbs/hpc/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Home-Improvement/zgbs/hi/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Jewelry/zgbs/jewelry/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Musical-Instruments/zgbs/musical-instruments/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0',
    'http://www.amazon.com/best-sellers-shoes/zgbs/shoes/ref=zg_bs_nav_0',
    'http://www.amazon.com/best-sellers-software/zgbs/software/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0',
    'http://www.amazon.com/best-sellers-video-games/zgbs/videogames/ref=zg_bs_nav_0',
    'http://www.amazon.com/Best-Sellers-Watches/zgbs/watches/ref=zg_bs_nav_0'
    ]

class Product:
    def __init__(self):
        self.url = ''
        self.reviews = ''
        self.weight = ''
        self.price = ''
        self.rank = ''

    def SaveToFile(product):
        pass


class Scraper:
    def __init__(self):
        self.file = open('AmazonBestSellerScraper.csv', 'w', newline='')
        self.file.write('{};{};{};{};{};\n'.format('url', 'Reviews', 'Weight', 'Price', 'Rank'))
        self.space = ''
        self.level = 0

    def analize(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        for item in soup.find_all('li',{'class':'zg_page'}):
            self.analizePageCatalog(item.a['href'])

    def analizeSubCatalog(self, url, level):

        self.level = self.level + 1
        self.space = self.space + ' '
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        hrefs = []
        space = '   '
        for item in soup.find_all('ul',{'id':'zg_browseRoot'}):
            for subitem in item.find_all(re.compile('^a'),{'href':re.compile(r'^http://www.amazon.com/Best-Sellers-.*\d+$')}):
                hrefs.append(subitem.get('href'))
        k = 0
        for k in range(level):
            del hrefs[0]
            print ('delete')

        for href in hrefs:
            print (level,href)
        if hrefs == []:
            print ('hrefs null')

    def analizePageCatalog(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content)

        for item in soup.find_all('div',{'class':'zg_itemWrapper'}):
            if item.find('div',{'class':'zg_itemImageImmersion'}) != None:
                url = re.sub("^\s+|\n|\r|\s+$", '', item.a['href']) #delete beg&end \n&\s
                if url !='':
                    self.analizePageProduct(url)
                else:
                    print ('empty url=')
                    self.file.write('empty url;;;;;\n')

    def analizePageProduct(self,url):
        product = Product()
        product.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content)

        item = soup.find('div',{'class':'fl gl5 mt3 txtnormal acrCount'})
        if item != None:
            product.reviews = item.text[1:-1]
        else:
            item = soup.find('span', {'id':'acrCustomerReviewText'},{'class':'a-size-base'})
            if item != None:
                product.reviews = item.text.split(' ')[0]

        for item in soup.find_all('tr',{'class':'shipping-weight'}):
            if item.find('td',{'class':'value'}) !=None:
                product.weight = item.find('td',{'class':'value'}).text[:-35]

        for item in soup.find_all('li'):
            if item.text.find('Shipping Weight:') !=-1:
                match =  re.search(u'\d+(?:\.\d+)?\s(pounds|ounces)', item.text)
                if match:
                    product.weight = match.group()
                else:
                    product.weight = ''

            if item.text.find('Amazon Best Sellers Rank:') !=-1:
                match =  re.search(u'\#\d+', item.text)
                if match:
                    product.rank = match.group()[1:]
                else:
                    product.rank =''

        for item in soup.find_all('span',{'class':'price'}):
            product.price = re.sub("^\s+|\n|\r|\s+$", '', item.text)

        for item in soup.find_all('b',{'class':'priceLarge kitsunePrice'}):
            product.price = re.sub("^\s+|\n|\r|\s+$", '', item.text)

        for item in soup.find_all('tr',{'id':'SalesRank'}):
            product.rank = item.text.split('\n')[23].split(' ')[0][1:]

        self.file.write('{};{};{};{};{};\n'.format(product.url, product.reviews, product.weight, product.price, product.rank))
        self.file.flush()

def main():
    start = time.clock()
    scraper = Scraper()
    scraper.analizeSubCatalog(urls[14],1)
    end = time.clock()
    print ('Time: %s' % (end - start))
if __name__ == '__main__':
    sys.exit(main())