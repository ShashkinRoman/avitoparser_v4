import os
import csv
from models_db import UrlsForParse, InformationFromAds
from config import session_db
from dotenv import load_dotenv
load_dotenv()


def find_request(session):
    dicts_with_date = []
    ads = session.query(InformationFromAds).all()
    for ad in ads:
        request_ = session.query(UrlsForParse).\
            filter(UrlsForParse.url == ad.url).first().request
        ads_ = {"phone": ad.phone,
                "request": request_,
                "name": ad.name,
                "title": ad.title,
                "price": ad.price,
                "place": ad.place,
                "description": ad.description,
                "type_ads": ad.type_ads,
                "region": ad.region,
                "url": ad.url}
        dicts_with_date.append(ads_)
    return dicts_with_date



def write_in_csv(dicts_with_date):
    path_csv = os.getenv('path_csv')
    with open(path_csv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('phone', 'request',
                         'name', 'title',
                         'price', 'place',
                         'description', 'type_ads',
                         'region', 'url'))
        for ad in dicts_with_date:
            writer.writerow((ad['phone'], ad['request'],
                             ad['name'], ad['title'],
                             ad['price'], ad['place'],
                             ad['description'], ad['type_ads'],
                             ad['region'], ad['url']))



def main():
    session = session_db()
    dicts_with_date = find_request(session)
    write_in_csv(dicts_with_date)


if __name__ == '__main__':
    main()
