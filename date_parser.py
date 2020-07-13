""""
берем данные из бд согласно статусу <10
пыаемся извлечь данные
если получилось кладем в другую бд из основной удаляем
если нет возвращаем обратно со статусом +=1
"""
import os
import random
from config import session_db
from models_db import UrlsForParse, InformationFromAds
from opera_driver import Operadriver, path as path_drivers
from time import sleep
from concurrent.futures.thread import ThreadPoolExecutor
# from selenium.common.exceptions import NoSuchElementException


def get_info_from_page(session, url, driver,
                       region, info_obj: list):
    sleep(random.randint(2, 5))
    url_page = "https://m.avito.ru" + url
    driver.get(url_page)
    sleep(2)
    try:
        check_publication = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div').text
    except:
        check_publication = "None"
    if check_publication == "" or "None":
        try:
            check_publication = driver.find_element_by_class_name('_1S_uy').text
        except:
            check_publication = "None"
    if check_publication == 'Снято с публикации':
        session.query(UrlsForParse). \
            filter(UrlsForParse.url == url). \
            update({"status": (UrlsForParse.status + 50)})
        print('Снято с публикации')
    else:
        try:
            name2 = driver.find_elements_by_class_name('MXmyi')
            name = name2[-1].text
        except:
            name = 'None'
            print('name None', url_page)
        try:
            title = driver.find_element_by_class_name('_3Yuc4').text
        except:
            title = 'None'
            print('title None', url_page)
        try:
            price = driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div[2]/p/span/meta[2]').get_attribute('content')
        except:
            price = 'None'
            try:
                if driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[2]/div[1]/div/div[1]/div/div[2]/p/span/span').text == 'Цена не указана':
                    price = 'Null'
                else:
                    price = 'None'
            except:
                pass
        if price == 'None':
            try:
                price = driver.find_elements_by_tag_name('meta')[1].get_attribute('content')
            except:
                price = 'None'
                print('price None', url_page)
        try:
            place = driver.find_element_by_class_name('lTQDM').text
        except:
            place = 'None'
            print('place None', url_page)
        try:
            description = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[3]/meta').get_attribute('content')
        except:
            description = "None"
        if description == "None":
            try:
                description = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div').text
            except:
                description = "None"
                print('description None', url_page)
        try:
            type_ads = driver.find_element_by_class_name('naQ7K').text
        except:
            type_ads = "None"
            print('type_ads None', url_page)
        # green button
        try:
            button_link = driver.find_element_by_class_name('dOyQe')
            button_link.click()
            sleep(1.5)
            phone_number = ''
            phone_number += driver.find_element_by_class_name('_3Ryy-').text[1:]
        except:
            phone_number = 'None'
            print('phone_number None', url_page)
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
        if ads_.get('phone') != "None":
            info_obj.append(ads_)
            a_db = InformationFromAds(**ads_)
            session.add(a_db)
            # session.query(UrlsForParse). \
            #     filter(UrlsForParse.url == url). \
            #     update({"status": (100)})
            print(ads_)
        else:
            session.query(UrlsForParse). \
                filter(UrlsForParse.url == url). \
                update({"status": (UrlsForParse.status + 1)})


def navigate_ads_for_thread(urls_regions, session, driver,
                            info_obj):
    counter = 0
    for u in urls_regions:
        try:
            urls_regions.remove(u)
            url = u[0]
            region = u[1]
            get_info_from_page(session, url, driver, region,
                            info_obj)
            counter += 1
        except Exception as e:
            print(e)
        if counter % 10 == 0:
            session.commit()

def main():
    session = session_db()
    urls_obj = session.query(UrlsForParse).filter(UrlsForParse.status < 10)
    info_obj = []
    driver_class = Operadriver()
    start_driver = driver_class.start_driver()
    # driver = driver_class.opera(start_driver, path[0])
    paths = path_drivers
    drivers = []
    urls_regions =[]
    [urls_regions.append((url.url, url.region)) for url in urls_obj]
    for path in paths:
        driver = driver_class.opera(start_driver, path)
        drivers.append(driver)

    with ThreadPoolExecutor(max_workers=2) as executor:
        for driver in drivers:
            try:
                executor.submit(navigate_ads_for_thread, urls_regions, session, driver,
                                info_obj)
            except IndexError as e:
                print('urls are over')
                print(e)
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
