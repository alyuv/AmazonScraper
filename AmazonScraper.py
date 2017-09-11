import sys
import re
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
SITE_URL = 'http://www.amazon.com'
URL = 'http://www.amazon.com/s/ref=nb_sb_noss/191-0790819-0139618?url=search-alias%3Dappliances&field-keywords='

urls =['http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dappliances&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Darts-crafts&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dautomotive&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dbaby-products&field-keywords=&rh=n%3A165796011&ajr=0',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dbeauty&field-keywords=&rh=n%3A3760911',
'http://www.amazon.com/Camera-Photo-Film-Canon-Sony/b/ref=sv_e_3?ie=UTF8&node=502394',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dmobile&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dapparel&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dcomputers&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Delectronics&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dhpc&field-keywords=&rh=n%3A3760901',
'http://www.amazon.com/b/ref=sr_aj?node=1055398&ajr=0',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dtools&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dindustrial&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Djewelry&field-keywords=',
'http://www.amazon.com/kitchen-dining-small-appliances-cookware/b/ref=topnav_storetab_k?ie=UTF8&node=284507',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dmi&field-keywords=',
'http://www.amazon.com/office-products-supplies-electronics-furniture/b/ref=topnav_storetab_op?ie=UTF8&node=1064954',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dlawngarden&field-keywords=',
'http://www.amazon.com/pet-supplies-dog-cat-food-bed-toy/b/ref=topnav_storetab_petsupplies?ie=UTF8&node=2619533011',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dshoes&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dsoftware&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dsporting&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dtoys-and-games&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dvideogames&field-keywords=',
'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dwatches&field-keywords=']

URL_CATEGORY_BEG = 'http://www.amazon.com/b/ref=s9_dnav_bw_ir02_'
URL_CATEGORY_END = '&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-6&pf_rd_r=1D2J6JAGAWANF3B3X0RN&pf_rd_t=101&pf_rd_p=1444632942&pf_rd_i=2619525011'

URL_SUBCATEGORY_BEG = 'http://www.amazon.com/b/ref=s9_dnav_bw_ir04_'
URL_SUBCATEGORY_END = '&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-6&pf_rd_r=0ETKRF43NJQPDMBNEMDC&pf_rd_t=101&pf_rd_p=1404938842&pf_rd_i=2645393011'


class Site:
    def __init__(self):
        self.categories = []

class Category:
    def __init__(self, url, title):
        self.subcategories =[]
        self.url = url
        self.title = title
        self.products =[]

class SubCategory:
    def __init__(self, url, title):
        self.url =''
        self.title = title
        self.products =[]

class Product:
    def __init__(self):
        self.url = ''
        self.name = ''
        self.reviews = ''
        self.weight = ''
        self.price = ''
        self.rank = ''

class Scraper:
    def __init__(self):
        if sys.version_info >= (3,0,0):
            self.csv_out = open("Amazon.csv",'w', newline='')
        else:
            self.csv_out = open("Amazon.csv",'wb')

    def analize(self,url):
        site = Site()
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        for listing in soup.find_all('a',{'class':'title ntTitle noLinkDecoration'}):
            if listing.find('div',{'class':'s9NavTitle'}) != None:
                url_category = URL_CATEGORY_BEG+ listing.get('href')[1:] + URL_CATEGORY_END
                category = Category(url_category,listing.get('title'))
                site.categories.append(category)
                response_category = requests.get(url_category)
                category_soup = BeautifulSoup(response_category.content)
                for link in category_soup.find_all('a',{'class':'title ntTitle noLinkDecoration'}):
                    if link.find('div',{'class':'s9NavTitle'}) != None:
                        url_subcategory = link.get('href')
                        if url_subcategory.find('www.amazon.com') ==-1:
                            url_subcategory = SITE_URL + url_subcategory
                        title = link.get('title')
                        print ('    ', title, url_subcategory)
                        subcategory = SubCategory(url_subcategory,link.get('title'))
                        category.subcategories.append(subcategory)

    def analizeNextPage(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        for list in soup.find_all('h3',{'class':'newaps'}):
            self.analizePageProduct(list.a['href'],list.a.span.text)

        for list in soup.find_all('a',{'class':'pagnNext'}):
            self.analizeNextPage('http://www.amazon.com/'+list.get('href'))

    def analizePageProduct(self,url, name):
        product = Product()
        product.url = url
        product.name = name
        response = requests.get(url)
        soup = BeautifulSoup(response.content)

        for list in soup.find_all('span', {'id':'acrCustomerReviewText'},{'class':'a-size-base'}):
            product.reviews = list.text.split(' ')[0]

        for list in soup.find_all('tr',{'class':'shipping-weight'}):
            if list.text.find('Weight') !=-1:
                product.weight = list.text.split(' ')[1][6:]

        for list in soup.find_all('span', {'id':'priceblock_ourprice'},{'class':'a-size-medium a-color-price'}):
            product.price = list.text

        for list in soup.find_all('tr', {'id':'SalesRank'}):
            product.rank = list.text.split('\n')[23].split(' ')[0][1:]

        print ('name={}, url={}, Reviews={}, Weight={}, Price={}, Rank={}'.format(product.name, product.url, product.reviews, product.weight, product.price, product.rank))
        self.mywriter.writerow([product.name, product.url, product.reviews, product.weight, product.price, product.rank])

    def analizeSubCategory(self,url):
        self.url= url
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        self.analizeNextPage(url)
        self.csv_out.close()

def main():
    scraper = Scraper()
    for i in range(len(urls)):
        scraper.analize(urls[i])

if __name__ == '__main__':
    sys.exit(main())
