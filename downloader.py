import sys
import bs4 as bs
from PyQt5.QtWidgets import QApplication
from helpers.dynamic_html import WebPage
from datasource import Postgres
from models.offer import OtodomOffers, OtodomDetials


class Downloader:

    def __init__(self, link, search, model, end_page=None):

        self.end_page = end_page
        self.link = link
        self.search = search
        print(search)
        self.model = model
        self.app = QApplication(sys.argv)
        self.webpage = WebPage(verbose=False)
        self.webpage.htmlReady.connect(self.my_html_processor)

    def save_results(self):
        print(len(self.html_offers))
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
        # print(self.html_offers)
        self.save_results()
        print('saved %s' % (url))

    def process(self):
        self.gen_urls()
        print('Processing list of urls...')
        self.webpage.process(self.urls)
        sys.exit(self.app.exec_())

    def gen_urls(self):
        self.urls = []
        if self.end_page:
            for i in range(2, int(self.end_page)+1):
                self.urls.append(self.link.format(i))
        else:
            self.urls.append(self.link)
            

    def find_offers_in_html(self):
        if isinstance(self.search, tuple):
            self.html_offers = self.soup.findAll(self.search[0], self.search[1])
        else:
            self.html_offers = self.soup.findAll(self.search)

    def create_from_html(self, item):
        return self.model.from_html(item)

    def save_to_file(self, filename, data):
        with open(filename, 'w+') as f:
            f.write(data)
