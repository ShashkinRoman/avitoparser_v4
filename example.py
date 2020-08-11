# from stem import Signal
# from stem.control import Controller
# import threading
# from selenium import webdriver
# # Смена IP тора (9151 и 9150 - это для браузера тор, для сервера будет 9050 9051 соотвественно)
# controller = Controller.from_port(port=9151)
# controller.authenticate()
# # Получение нового адреса
#
# controller.signal(Signal.NEWNYM)
#
# controller.close()  # отключение от тора
#
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('--proxy-server=socks5://127.0.0.1:9150')


import os
import sys
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
import argparse
load_dotenv()


def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument("-reg", "--region", nargs='+', required=True,
                    help="request for parse example: beauty_large, beauty_small, beauty_msk_mo or '[msk, ...]'")
    parser.add_argument("-req", "--requests", nargs='+', required=True,
                    help="request for parse example: ресницы,брови")
    parser.add_argument("-db", "--database", required=True,
                    help="database for parse example: beauty_large, beauty_small, beauty_msk_mo")
    parser.add_argument("-t", "--type", required=True,
                    help="category for parse example:  beauty, nedvij")
    return parser


def check_args(parser):
    # parser = create_parser()
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
    requests = namespace.requests
    database = namespace.database
    type = namespace.type
    return regions, requests, database, type



def main():
    parser = create_parser()
    regions, requests, database, type = check_args(parser)
    print(regions, requests, database, type)

if __name__ == '__main__':
    main()

#
#
#
# for name in namespace.test:
# 	print("Привет, {}!".format(name))

# args = vars(ap.parse_args())
# # display a friendly message to the user
# print("Hi there {}, it's nice to meet you!".format(args["name"]))
#
# # if args["test"] == "one":
# #     print("test arg =  {}".format(args["test"]))
#
# count = 0
# for a in args['test']:
# 	count += 1
# 	print(a, count)
