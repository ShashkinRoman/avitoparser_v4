import random
from config import main as conf_main
from models_db import UrlsForParse, InformationFromAds, session_db
from opera_driver import Operadriver, path as path_drivers
from time import sleep
from concurrent.futures.thread import ThreadPoolExecutor
from selenium.common.exceptions import NoSuchElementException


def get_info_from_page(session, url, driver,
                       region, info_obj: list, request):
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
            name = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[3]/div/div[1]/div/div[1]/div/h1').text
        except:
            name = 'None'
            print('name None', url_page)
        try:
            title = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div[1]/div/h1').text
        except:
            title = 'None'
            print('title None', url_page)
        try:
            price = driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[3]/div/div[1]/div/div[2]/p/span/span').text[:-2]
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
        try:
            place = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[3]/div/div[4]/div/button/span[1]').text
        except:
            place = 'None'
            print('place None', url_page)
        try:
            description = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[4]/div[2]/div[1]/div').text
        except:
            description = "None"
            print('description None', url_page)
        try:
            type_ads = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[5]/div/a/div/div/div[1]/span[3]').text
        except:
            type_ads = "None"
            print('type_ads None', url_page)
        # green button
        try:
            button_link = driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[3]/div/div[2]/div/div/div[1]/div[1]')
            button_link.click()
            sleep(2)
            # phone_number = ''
            phone_number = driver.find_element_by_xpath('//*[@id="modal"]/div[2]/div/div[1]/span[2]').text[1:]
        except NoSuchElementException:
            phone_number = 'None'
            print('NoSuchElementException for phone number')
        except Exception:
            if button_link.text == 'Написать':
                phone_number = 'Null'
            else:
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
                "request": request,
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
            request = u[2]
            get_info_from_page(session, url, driver, region,
                            info_obj, request)
            counter += 1
        except Exception as e:
            print(e)
        if counter % 10 == 0:
            session.commit()


def main():
    regions, requests_, url_generator, object_parse, database, threads = conf_main()
    # database = 'test_beauty'
    session = session_db(database)
    urls_obj = session.query(UrlsForParse).filter(UrlsForParse.status < 10)
    info_obj = []
    driver_class = Operadriver()
    start_driver = driver_class.start_driver()
    paths = path_drivers
    drivers = []
    urls_regions = []
    [urls_regions.append((url.url, url.region, url.request)) for url in urls_obj]
    for path in paths[:threads]:
        try:
            driver = driver_class.opera(start_driver, path)
            drivers.append(driver)
        except:
            pass

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for driver in drivers:
            try:
                executor.submit(navigate_ads_for_thread, urls_regions, session, driver,
                                info_obj)
            except IndexError as e:
                # print('urls are over')
                print(e)
            session.commit()
    print("added ads {}".format(len(info_obj)))


if __name__ == '__main__':
    main()
