from abc import ABC
from dataclasses import dataclass
from datasource import Postgres
from config import Config


@dataclass
class OfferItem:
    title: str = None
    url: str = None
    id: str = None
    remote_agent: str = None
    developer_offer_title: str = None
    address: str = None
    total_price: str = None
    unit_price: str = None
    unit_size: str = None
    size: str = None
    offer_type: str = None
    publication_date: str = None

@dataclass
class OfferDetails:
    details: str
    description: str
    offer_id: int
    add_date: str
    update_date: str

class OtodomDetials:
    def __init__(self, offer_details):
        self.offer_details = offer_details
        # print(self.offer_details)

    @classmethod
    def from_html(cls, article):
        # print(8*'####****')
        # print(article)
        # print(8*'****')
        offer = OfferDetails(
            description=cls.get_from_article(
                article,'div', 'css-rwppy9 e1r1048u1'),
            details=cls.get_from_article(
                article, 'div', 'css-1d9dws4 egzohkh2'),
            offer_id=cls.get_from_article(
                article, 'div', 'css-jjerc6 euuef473')[20:],
            add_date=cls.get_from_article(
                article, 'div', 'css-gqksao euuef471'),
            update_date=cls.get_from_article(
                article, 'div', 'css-yrwank euuef470'),
        )
        print(offer.offer_id, type(offer.offer_id))
        return cls(offer)

    @staticmethod
    def get_from_article( article, tag, class_):
        found = article.find(tag, class_=class_)
        foudn_text = OtodomOffers.get_text_or_tag(found)
        return foudn_text

    @staticmethod
    def get_text_or_tag(tag):
        try:
            response = ' '.join(tag.contents)
            return response.strip()
        except:
            return tag

    def save_to_db(self):
        db = Postgres(Config.DSN)
        try:
            db.execute(
                '''
                INSERT INTO public.otodom_details
                (details, description, otodom_id, add_date, update_date)
                VALUES(%s, %s, %s, %s, %s);
                ''',[
                    str(self.offer_details.details),
                    str(self.offer_details.description),
                    int(self.offer_details.offer_id),
                    str(self.offer_details.add_date),
                    str(self.offer_details.update_date),
                    ]
                )
        except Exception as e:
            print(e)
        db.commit()

class OtodomOffers:
    def __init__(self, offer):
        self.offer = offer

    @classmethod
    def from_html(cls, article):

        offer = OfferItem(
            title=cls.get_from_article(
                article,'span', 'offer-item-title'),
            unit_size=cls.get_from_article(
                article, 'li', 'offer-item-area'),
            unit_price=cls.get_from_article(
                article, 'li', 'offer-item-price-per-m'),
            total_price=cls.get_from_article(
                article, 'li', 'offer-item-price'),
            size=cls.get_from_article(
                article, 'li', 'offer-item-rooms'),
            offer_type=cls.get_from_article(
                article, 'li', 'pull-right'),
            address=cls.get_from_article(
                article, 'p','text-nowrap'),
            remote_agent=cls.get_from_article(article, 'li', 'remote-agent'),
            developer_offer_title=cls.get_from_article(
                article, 'div', 'developer-offer-title'),
            id=article['id'],
            url=article['data-url']
        )
        return cls(offer)

    @staticmethod
    def get_from_article( article, tag, class_):
        found = article.find(tag, class_=class_)
        foudn_text = OtodomOffers.get_text_or_tag(found)
        return foudn_text

    @staticmethod
    def get_text_or_tag(tag):
        try:
            response = ' '.join(tag.contents)
            return response.strip()
        except:
            return tag

    def save_to_db(self):
        db = Postgres(Config.DSN)
        try:
            db.execute(
                '''
                INSERT INTO otodom(
                    title,
                    id_otodom,
                    remote_agent,
                    developer_offer_title,
                    address,
                    total_price,
                    unit_price,
                    unit_size,
                    size,
                    offer_type,
                    url
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ''',[
                    str(self.offer.title),
                    str(self.offer.id),
                    str(self.offer.remote_agent),
                    str(self.offer.developer_offer_title),
                    str(self.offer.address),
                    str(self.offer.total_price),
                    str(self.offer.unit_price),
                    str(self.offer.unit_size),
                    str(self.offer.size),
                    str(self.offer.offer_type),
                    str(self.offer.url)
                    ]
                )
        except Exception as e:
            print(f'DB SAVE ERROR {str(e)}')
        db.commit()


class MorizonOffers:
    def __init__(self, offer):
        self.offer = offer

    @classmethod
    def from_html(cls, article):

        try:
            id=article['data-id']
        except:
            raise KeyError
        offer = OfferItem(
            id = id,
            title=cls.get_from_article(
                article,'h2', 'single-result__title'),
            unit_size=cls.get_from_article(
                article, 'ul', "param list-unstyled list-inline").findAll('li')[1].text.strip(),
            unit_price=cls.get_from_article(
                article, 'p', "single-result__price single-result__price--currency"),
            total_price=cls.get_from_article(
                article, 'p', "single-result__price"),
            size=cls.get_from_article(
                article, 'ul', "param list-unstyled list-inline").findAll('li')[0].text.strip(),
            developer_offer_title=cls.get_from_article(
                article, 'div', "description single-result__description").text.strip(),
            publication_date=cls.get_from_article(article,
                'span', 'single-result__category single-result__category--date'
                ),
            url=cls.get_from_article(
                    cls.get_from_article(article, 'header'),
                    'a',
                    'property_link property-url')['href']
            )
        return cls(offer)


    @staticmethod
    def get_from_article(article, tag, class_=None):
        if not class_:
            found = article.find(tag)
        else:
            found = article.find(tag, class_=class_)
        foudn_text = MorizonOffers.get_text_or_tag(found)
        return foudn_text

    @staticmethod
    def get_text_or_tag(tag):
        try:
            response = ' '.join(tag.contents)
            return response.strip()
        except:
            return tag

    def save_to_db(self):
        db = Postgres(Config.DSN)
        try:
            db.execute(
                '''
                INSERT INTO morizon(
                    title,
                    id_morizon,
                    publication_date,
                    developer_offer_title,
                    total_price,
                    unit_price,
                    unit_size,
                    size,
                    url
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ''',[
                    str(self.offer.title),
                    str(self.offer.id),
                    str(self.offer.publication_date),
                     str(self.offer.developer_offer_title),
                     str(self.offer.total_price),
                     str(self.offer.unit_price),
                     str(self.offer.unit_size),
                     str(self.offer.size),
                     str(self.offer.url)
                    ]
                )
        except:
            print('Not saved ', self.offer)

        db.commit()

