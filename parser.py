"""
Сделать:
регион, возможность парсить подряд несколько регионов
Проверка, если встречает больше 10 объявлений, которые уже есть в базе, то останавливается
Решить проблему с переадресацией
Проверка работы с бд:
 - Сделать дефолтные значения NULL для всех полей кроме URL
 - Проверка. Пробуем получить данные для всех строк у которых phone == NULL
 - Если ссылка на страницу возвращает 404, то удаляем строку
 -
каталог баз данных(папка в которой лежат бд)
"""

from time import sleep
from config import main as config_main
from concurrent.futures.thread import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from webdriver import webdriver_conf
from config import InformationFromAds
from datetime import datetime, timedelta


def get_urls_from_page(url_page, ads_obj, session, i):
    """check url in base and write, if not found
    if get ban from avito sleep on 30 min and print time"""
    html = requests.get(url_page).text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all(attrs={"class": "item__line"})
    # check len ads_onj on 10 page, for understand have ban or no.
    # If have, sleep 30 min and write sleep time, and restart function
    if i == 5:
        if len(ads_obj.urls_ads) == 0:
            clock_in_half_hour = datetime.now() + timedelta(minutes=30)
            print(f'ban from avito {datetime.today().strftime("%Y-%m-%d-%H.%M")}, '
                  f'sleep until {clock_in_half_hour.strftime("%Y-%m-%d-%H.%M")}')
            sleep(1800)
            get_urls_from_page(url_page, ads_obj, session)
    counter = 0
    for page in pages:
        link = page.find_all(attrs={"class": "snippet-link"})[0]
        # check url in database and skip if have
        try:
            session.query(InformationFromAds).filter(
                InformationFromAds.url == link.attrs['href']).one()
            counter += 1
            if counter == 30:
                break
        except:  # todo add check 'NoResultFound' and write in base
            ads_obj.urls_ads.append(link.attrs['href'])


def get_info_from_page(ads_obj, regions):
    driver = webdriver_conf.Webdriver().func_webdriver()
    for url in ads_obj.urls_ads:
        url_page = "https://m.avito.ru" + url
        ads_obj.urls_ads.remove(url)
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
                '//*[@id="app"]/div/div[2]/div[3]/div/div[1]/div/div[2]/p/span/span').text
        except:
            price = 'None'
        try:
            place = ''
            place += driver.find_element_by_class_name('lTQDM').text
        except:
            place = 'None'
        try:
            description = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[4]/div[2]/div/div').text
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
                "region": regions,
                "url": url}
        print(ads_)
        ads_obj.info_ads.append(ads_)
    driver.close()


# все переменные для ввода хранятся в .env
def main():
    av_request, regions, ads_obj, url_generator, session = config_main()
    urls = url_generator.urls(regions, av_request)
    with ThreadPoolExecutor(max_workers=2) as executor:
        for i in range(1, 30):
            url_page = urls + str(i)
            threads_ads = executor.submit(get_urls_from_page, url_page, ads_obj, session, i)


    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(get_info_from_page, ads_obj, regions)
        sleep(2)

    for ad in ads_obj.info_ads:
        ad_db = InformationFromAds(**ad)
        session.add(ad_db)
    session.commit()


if __name__ == '__main__':
    main()
