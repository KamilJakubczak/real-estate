import sys
from downloader import Downloader
from models.offer import OtodomOffers, MorizonOffers, OtodomDetials

import bs4 as bs

def from_file():
    with open('test.html', 'r') as f:
        html = f.read()
    
    soup = bs.BeautifulSoup(html, 'lxml')
    offers = soup.findAll('div', 'css-rwppy9 e1r1048u1')
    save_results(offers)

providers = {
    'morizon': {
        'model': MorizonOffers,
        'link': 'https://www.morizon.pl/mieszkania/warszawa/bemowo/?page={}',
        'search': ('div', 'row row--property-list')
    },

    'otodom': {
        'model': OtodomOffers,
        'link': 'https://www.otodom.pl/sprzedaz/mieszkanie/lodz/?search%5Bregion_id%5D=5&search%5Bcity_id%5D=1004&nrAdsPerPage=72',
        'search': 'article' 
    }
}

        #'link': 'https://www.otodom.pl/sprzedaz/mieszkanie/lodz/?search%5Bcity_id%5D=26&nrAdsPerPage=72',
if __name__ == '__main__':
    if sys.argv[1] == '-f':
        from_file()
    
    if sys.argv[1] == '-e':
        site = sys.argv[2]
        end_page = sys.argv[3]
        model = providers[site]['model']
        link = providers[site]['link']
        search = providers[site]['search']
        p = Downloader(link, search, model, end_page)
        p.process()

    if sys.argv[1] == 'test':
        link = 'https://www.otodom.pl/pl/oferta/mieszkanie-2-pokoje-po-generalnym-remoncie-bemowo-ID4aIOq.html#c4e497c5f1'
        # search = 'css-rwppy9 e1r1048u1' # opis
        # search = 'css-1acw23q e1t9fvcw4'
        search = ('div', 'css-1acw23q e1t9fvcw4')
        model = OtodomDetials
        p = Downloader(link, search, model)
        p.process()
