""""
берем данные из бд согласно статусу <10
пыаемся извлечь данные
если получилось кладем в другую бд из основной удаляем
если нет возвращаем обратно со статусом +=1
"""
import random
from config import session_db
from models_db import UrlsForParse, InformationFromAds
from opera_driver import driver as dr
from time import sleep


def get_info_from_page(session, url, driver,
                       region, info_obj: list):
    sleep(random.randint(2, 5))
    url_page = "https://m.avito.ru" + url
    driver.get(url_page)
    sleep(2)
    try:
        name2 = driver.find_elements_by_class_name('MXmyi')
        name = name2[-1].text
    except:
        name = 'None'
    try:
        title = driver.find_element_by_class_name('_3Yuc4').text
    except:
        title = 'None'
    try:
        price = driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div[2]/p/span/meta[2]').get_attribute('content')
    except:
        price = 'None'
    try:
        place = driver.find_element_by_class_name('lTQDM').text
    except:
        place = 'None'
    try:
        description = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[3]/meta').get_attribute('content')
    except:
        description = "None"
    try:
        type_ads = driver.find_element_by_class_name('naQ7K').text
    except:
        type_ads = "None"
    # green button
    try:
        button_link = driver.find_element_by_class_name('dOyQe')
        button_link.click()
        sleep(1)
        phone_number = ''
        phone_number += driver.find_element_by_class_name('_3Ryy-').text[1:]
    except:
        phone_number = 'None'
    # blue button
    # try:
    #     button_link = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[8]/div/div/div/a[1]')
    #     button_link.click()
    #     sleep(1)
    #     phone_number = driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[1]/span[2]').text[1:]
    # except:
    #     phone_number = 'None'
    ads_ = {"phone": phone_number,
            "name": name,
            "title": title,
            "price": price,
            "place": place,
            "description": description,
            "type_ads": type_ads,
            "region": region,
            "url": url}
    values = list(ads_.values())
    if values.count('None') == 0:
        info_obj.append(ads_)
        a_db = InformationFromAds(**ads_)
        session.add(a_db)
        # session.query(UrlsForParse). \
        #     filter(UrlsForParse.url == url). \
        #     update({"status": (100)})
        print(ads_)
    else:
        session.query(UrlsForParse).\
            filter(UrlsForParse.url == url). \
            update({"status": (UrlsForParse.status + 1)})


def main():
    session = session_db()
    urls_obj = session.query(UrlsForParse).filter(UrlsForParse.status < 10)
    info_obj = []
    driver = dr
    counter = 0
    for u in urls_obj:
        try:
            url = u.url
            region = u.region
            get_info_from_page(
                session, url, driver, region,
                info_obj)
            counter += 1
        except Exception as e:
            print(e)
        if counter % 10 == 0:
            session.commit()
    session.commit()
    print("added ads {}".format(len(info_obj)))
    #
    # for a in info_obj:
    #     a_db = InformationFromAds(**a)
    #     session.add(a_db)
    # session.commit()
    # print("added ads {}".format(info_obj))


if __name__ == '__main__':
    main()
