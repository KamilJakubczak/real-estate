from abc import ABC
from dataclasses import dataclass
from datasource import Postgres


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
        # print(article['data-url'])
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
        db = Postgres()
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
        except:
            pass
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
    def get_from_article( article, tag, class_=None):
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
        db = Postgres()
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
            pass
        db.commit()

