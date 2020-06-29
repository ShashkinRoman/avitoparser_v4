# todo придумать способ как импортировать списки регионов и запросов
# todo нужно проверять страницу блокировки, а не счетчики, потому что может не быть обхектов на странице
import os
import json
import requests
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures.thread import ThreadPoolExecutor
from config import Urls, session_db
from models_db import UrlsForParse, session_db
from sqlalchemy.orm.exc import NoResultFound
from dotenv import load_dotenv
load_dotenv()


def get_urls_from_page(url_page, ads_obj, session, request, region):
    """check url in base and write, if not found
    if get ban from avito sleep on 30 min and print time"""
    html = requests.get(url_page).text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all(attrs={"class": "item__line"})
    # check len ads_onj on 10 page, for understand have ban or no.
    # If have, sleep 30 min and write sleep time, and restart function
    # if i == 5:
    #     if len(ads_obj.urls_ads) == 0:
    #         clock_in_half_hour = datetime.now() + timedelta(minutes=30)
    #         print(f'ban from avito {datetime.today().strftime("%Y-%m-%d-%H.%M")}, '
    #               f'sleep until {clock_in_half_hour.strftime("%Y-%m-%d-%H.%M")}')
    #         sleep(1800)
    #         get_urls_from_page(url_page, ads_obj, session)
    counter = 0
    for page in pages:
        link = page.find_all(attrs={"class": "snippet-link"})[0]
        # check url in database and skip if have
        try:
            session.query(UrlsForParse).filter(
                UrlsForParse.url == link.attrs['href']).one()
            print('jopa')
        except NoResultFound:
            ads_obj.append({'request': request,
                            'region': region,
                            'date': datetime.now(),
                            'url': link.attrs['href'],
                            'status': 0,
                            })



        # except:  # todo add check 'NoResultFound' and write in base
        #     ads_obj.urls_ads.append(link.attrs['href'])
        # 

def main():
    regions = json.loads(os.getenv('regions_for_pars'))
    requests_ = json.loads(os.getenv('requests'))
    session = session_db()
    ads_obj = []
    for region in regions:
        for request in requests_:
            url = Urls().urls(region, request)
            with ThreadPoolExecutor(max_workers=2) as executor:
                for i in range(1, 30):
                    url_page = url + str(i)
                    threads_ads = executor.submit(
                        get_urls_from_page, url_page, ads_obj,
                        session, i, request, region)


    pass


if __name__ == '__main__':
    main()
