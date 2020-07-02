import os
from builtins import object
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fake_useragent import UserAgent
load_dotenv()


def proxy_parse(url_proxy):
    html = requests.get(url_proxy).text
    soup = BeautifulSoup(html, 'html.parser')
    ip_list = soup.find_all("input", class_="ch")
    for i in range(0, len(ip_list)):
        ip_list[i] = ip_list[i]['value']
    return ip_list


def header_proxy(proxy_list):
    proxy = proxy_list.pop(0)
    proxy_list.append(proxy)
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    proxies = {"http": "http://{}".format(proxy),
               # "https": "http://{}".format(proxy)
               }
    return header, proxies


class Ads:
    """ Принимает урлы каждого из объявлений
    и информацю для последующей записи в бд """
    def __init__(self):
        self.urls_ads = []
        self.info_ads =[]


def avito_request():
    """ декодируем, чтобы русские символы корректо вставлялись в урл
    :return: запрос на русском в кодировке UTF-8 """
    decode_request = os.getenv('request_avito')
    request_avito = decode_request.encode('cp1251').decode('utf-8')
    return request_avito


class Urls(object):
    """ В зависимости от object_parse выбирает вариант сборки урла
    возвращает шаблон урла каталога """
    def __init__(self):
        self.object_parse = os.getenv('object_parse')

    def urls(self, region, avito_request):
        if self.object_parse == 'beauty':
            url = 'https://www.avito.ru/' + region\
                  + '/predlozheniya_uslug/krasota_zdorove-ASgBAgICAUSYC6qfAQ?q='\
                  + avito_request + '&p='

        if self.object_parse == 'nedvij_studii_vtorich':
            url = 'https://www.avito.ru/' + region \
                  + '/kvartiry/prodam/studii/vtorichka-ASgBAQICAUSSA8YQAkDmBxSMUsoIFP5Y' \
                  + avito_request + '?p='
        return url


Base = declarative_base()


class InformationFromAds(Base):
    __tablename__ = os.getenv('tablename')
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    name = Column(String)
    title = Column(String)
    price = Column(String)
    place = Column(String)
    description = Column(String)
    type_ads = Column(String)
    region = Column(String)
    url = Column(String)

    def __init__(self, phone, name, title, price, place, description, type_ads, region, url):
        self.phone = phone
        self.name = name
        self.title = title
        self.price = price
        self.place = place
        self.description = description
        self.type_ads = type_ads
        self.region = region
        self.url = url

    def __repr__(self):
        return "<InformationFromAds('%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s')>"\
               % (self.phone, self.name, self.title,
                  self.price, self.place, self.description,
                  self.type_ads, self.region, self.url)


def session_db():
    engine = create_engine('sqlite:///' + os.getenv('database_name') + '.db',
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    session_object = sessionmaker()
    session_object.configure(bind=engine)
    Base.metadata.create_all(engine)
    session = session_object()
    return session


# test = InformationFromAds('phone', 'name', 'title', 'price', 'place', 'description', 'type_ads', 'region', 'url')
def main():
    # av_request = avito_request()
    av_request = os.getenv('request_avito')
    regions = os.getenv('regions')
    ads_obj = Ads()
    # object_parse = os.getenv('object_parse') #указываем для выбора формы урла
    url_generator = Urls()
    session = session_db()
    return av_request, regions, ads_obj, url_generator, session


if __name__ == '__main__':
    main()
