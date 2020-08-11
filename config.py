import os
import sys
from builtins import object
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from fake_useragent import UserAgent
import argparse
load_dotenv()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-reg", "--region", nargs='+', default=['balakovo'],
                        help="request for parse example: beauty_large, beauty_small, beauty_msk_mo or '[msk, ...]'")
    parser.add_argument("-req", "--requests", nargs='+', default=['ресницы'],
                        help="request for parse example: ресницы,брови")
    parser.add_argument("-db", "--database", default='beauty',
                        help="database for parse example: beauty_large, beauty_small, beauty_msk_mo")
    parser.add_argument("-t", "--type", default='beauty',
                        help="category for parse example:  beauty, nedvij")
    parser.add_argument("-th", "--threads", default='1',
                        help="number threads, default 1")
    return parser


def check_args():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.region == ['beauty_large']:
        regions = ["novosibirsk", "ekaterinburg", "nizhniy_novgorod", "kazan", "chelyabinsk", "omsk", "samara",
                   "rostov-na-donu", "ufa", "krasnoyarsk", "voronezh", "perm", "volgograd", "krasnodar", "saratov",
                   "tyumen", "tolyatti", "izhevsk", "barnaul", "ulyanovskaya_oblast", "irkutsk"]
    if namespace.region == ['beauty_small']:
        regions = ["habarovsk", "yaroslavl", "vladivostok", "mahachkala", "mahachkala", "orenburg", "kemerovo",
                   "novokuznetsk", "ryazan", "astrahan", "naberezhnye_chelny", "penza", "kirovskaya_oblast_kirov",
                   "lipetsk", "cheboksary", "balashiha", "kaliningrad", "tula", "kursk", "sevastopol", "sochi",
                   "stavropol", "ulan-ude", "tver", "magnitogorsk", "ivanovo", "bryansk", "belgorod", "vladimir",
                   "surgut", "nizhniy_tagil", "chita", "arhangelsk", "simferopol", "kaluga", "smolensk",
                   "volgogradskaya_oblast_volzhskiy", "yakutsk", "saransk", "cherepovets", "kurgan", "vologda",
                   "orel", "vladikavkaz", "podolsk", "groznyy", "murmansk", "tambov", "petrozavodsk", "sterlitamak",
                   "nizhnevartovsk", "kostroma", "novorossiysk", "yoshkar-ola", "himki", "taganrog",
                   "komsomolsk-na-amure", "syktyvkar", "nizhnekamsk", "nalchik", "shahty", "dzerzhinsk", "orsk",
                   "bratsk", "amurskaya_oblast_blagoveschensk", "engels", "angarsk", "korolev", "velikiy_novgorod",
                   "staryy_oskol", "mytischi", "pskov", "lyubertsy", "yuzhno-sahalinsk", "biysk", "prokopevsk",
                   "armavir", "kaluga", "smolensk", "volgogradskaya_oblast_volzhskiy", "yakutsk", "saransk",
                   "cherepovets", "kurgan", "vologda", "orel", "vladikavkaz", "podolsk", "groznyy", "murmansk",
                   "tambov", "petrozavodsk", "sterlitamak", "nizhnevartovsk", "kostroma", "novorossiysk",
                   "yoshkar-ola", "himki", "taganrog", "komsomolsk-na-amure", "syktyvkar", "nizhnekamsk", "nalchik",
                   "shahty", "dzerzhinsk", "orsk", "bratsk", "amurskaya_oblast_blagoveschensk", "engels", "angarsk",
                   "korolev", "velikiy_novgorod", "staryy_oskol", "mytischi", "pskov", "lyubertsy", "yuzhno-sahalinsk",
                   "biysk", "prokopevsk", "armavir"]
    if namespace.region == ['msk_mo']:
        regions = ["moskva", "moskovskaya_oblast"]
    else:
        regions = namespace.region
    requests = namespace.requests
    database = namespace.database
    type_ = namespace.type
    threads = int(namespace.threads)
    return regions, requests, database, type_, threads


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
    def __init__(self, obj_pars):
        self.object_parse = obj_pars

    def urls(self, region, avito_request):
        if self.object_parse == 'beauty':
            url = 'https://www.avito.ru/' + region\
                  + '/predlozheniya_uslug/krasota_zdorove-ASgBAgICAUSYC6qfAQ?q='\
                  + avito_request + '&p='

        if self.object_parse == 'nedvij_studii_vtorich':
            url = 'https://www.avito.ru/' + region \
                  + '/kvartiry/prodam/studii/vtorichka-ASgBAQICAUSSA8YQAkDmBxSMUsoIFP5Y' \
                  + avito_request + '?p='
        if self.object_parse == 'transport_perevozki':
            url = 'https://www.avito.ru/' + region \
                  + '/predlozheniya_uslug/transport_perevozki-ASgBAgICAUSYC8SfAQ' + '?p='
                  # + avito_request + \

        return url


def main():
    regions, av_request, database, object_parse, threads = check_args()
    url_generator = Urls(object_parse)
    return regions, av_request, url_generator, object_parse, database, threads


if __name__ == '__main__':
    main()
