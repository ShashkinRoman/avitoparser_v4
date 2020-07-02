# todo проверять не только из бд есть ли дубли, но и из тез которые уже спарсили
import os
import json
import random
import requests
from requests.exceptions import ProxyError, ChunkedEncodingError, ConnectionError
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import Urls, session_db, proxy_parse, header_proxy
from models_db import UrlsForParse, session_db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from fake_useragent import UserAgent
from dotenv import load_dotenv
load_dotenv()


def get_urls_from_page(url_page, ads_obj, session, request, region, proxy_list: list, counter_proxy):
    """

    :param url_page:
    :param ads_obj:
    :param session:
    :param request:
    :param region:
    :param proxy_list:
    :param counter_proxy:
    :return:
    """

    try:
        header, proxies = header_proxy(proxy_list)
        html = requests.get(url_page, headers=header, proxies=proxies).text
    except ProxyError or ChunkedEncodingError or ConnectionError:
        get_urls_from_page(url_page, ads_obj, session, request, region, proxy_list)
        print('change proxy')
        counter_proxy +=1
        if counter_proxy == len(proxy_list):
            print("all proxy used and don't work")
    # html = requests.get(url_page, proxies=proxies).text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all(attrs={"class": "item__line"})
    counter = 0
    for page in pages:
        link = page.find_all(attrs={"class": "snippet-link"})[0]
        try:
            session.query(UrlsForParse).filter(
                UrlsForParse.url == link.attrs['href']).one()
            counter += 1
        except MultipleResultsFound:
            counter += 1
        except NoResultFound:
            ads_obj.append({'request': request,
                            'region': region,
                            'date': datetime.now(),
                            'url': link.attrs['href'],
                            'status': 0,
                            })
        if counter >= 50:
            break
    # print('query {}, region {} is over, {}'.format(request, region, datetime.now()))
    check = len(ads_obj)
    return check


def main():
    regions = json.loads(os.getenv('regions_for_pars'))
    requests_ = json.loads(os.getenv('requests'))
    proxy_list = proxy_parse(os.getenv('url_proxy'))
    for region in regions:
        for request in requests_:
            session = session_db()
            ads_obj = []
            url = Urls().urls(region, request)
            counter = 0
            for i in range(1, 100):
                start = len(ads_obj)
                counter_proxy = 0
                # print(start)
                sleep(random.randint(1, 2))
                url_page = url + str(i)
                end = get_urls_from_page(url_page, ads_obj,
                                         session, request, region,
                                         proxy_list, counter_proxy)
                # print(end)
                # print(i)
                if start == end:
                    counter += 1
                    if counter == 5:
                        break

            for a in ads_obj:
                a_db = UrlsForParse(**a)
                session.add(a_db)
            session.commit()
            print('quantity added urls {} query {}, region {} is over, {}'
                  .format(len(ads_obj), request, region, datetime.now()))
            session.close()


if __name__ == '__main__':
    main()
