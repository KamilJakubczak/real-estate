import sys
import bs4 as bs
from PyQt5.QtWidgets import QApplication
from helpers.dynamic_html import WebPage
from datasource import Postgres
from models.offer import OtodomOffers, MorizonOffers
from abc import ABC


class Downloader(ABC):

    def __init__(self, end_page):

        self.end_page = end_page
        self.app = QApplication(sys.argv)
        self.webpage = WebPage(verbose=False)
        self.webpage.htmlReady.connect(self.my_html_processor)

    def save_results(self):
        for item in self.html_offers:
            try:
                offer = self.create_from_html(item)
                offer.save_to_db()
            except (KeyError, AttributeError) as e:
                print(str(e))
                pass

    def my_html_processor(self, html, url):
        self.soup = bs.BeautifulSoup( html, 'lxml')
        self.find_offers_in_html()
        self.save_results()
        print('saved %s' % (url))

    def process(self):
        self.gen_urls()
        print('Processing list of urls...')
        self.webpage.process(self.urls)
        sys.exit(self.app.exec_())

    def gen_urls(self):
        self.urls = []
        for i in range(2, int(self.end_page)+1):
            self.urls.append(self.link.format(i))

    def find_offers_in_html(self):
        self.html_offers = self.soup.findAll(self.search)

    def create_from_html(self, item):
        return self.model.from_html(item)

class OtodomDownloader(Downloader):
    
    # Bemowo z filtrami
    # link = 'https://www.otodom.pl/sprzedaz/mieszkanie/warszawa/?search%5Bfilter_float_price%3Ato%5D=500000&search%5Bfilter_float_m%3Afrom%5D=40&search%5Bfilter_float_build_year%3Afrom%5D=1990&search%5Bcity_id%5D=26&nrAdsPerPage=72&page={}'
    # Warszawa
    link = 'https://www.otodom.pl/sprzedaz/mieszkanie/warszawa/?search%5Bcity_id%5D=26&nrAdsPerPage=72'
    search = 'article' 
    model = OtodomOffers

class MorizonDownloader(Downloader):
    link = 'https://www.morizon.pl/mieszkania/warszawa/bemowo/?page={}'
    search = 'div', 'row row--property-list'
    model = MorizonOffers

        
def from_file():
    with open('testyy.html', 'r') as f:
        html = f.read()
    
    soup = bs.BeautifulSoup(html, 'lxml')
    offers = soup.findAll('div', 'row row--property-list')
    save_results(offers)

providers = {
    'morizon': MorizonDownloader,
    'otodom': OtodomDownloader
}

if __name__ == '__main__':
    if sys.argv[1] == '-f':
        from_file()
    
    if sys.argv[1] == '-e':
        p = providers[sys.argv[2]](sys.argv[3])
        p.process()

