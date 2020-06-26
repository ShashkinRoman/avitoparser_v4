# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
# from stem import Signal
# from stem.control import Controller
load_dotenv()


class Webdriver():
    def __init__(self, driver_=1):
        self.driver = driver_

    def func_webdriver(self):  # todo переделать на класс, чтобы вызывая экземляр класса оставалась одна и та же сессия
        options = Options()
        path = os.getenv('chrome_driver')
        mobile_emulation = {"deviceName": "Nexus 5"}
        # options.add_argument("--disable-notifications")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        # options.add_argument('headless')
        # options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
        # controller = Controller.from_port(port=9151)
        # controller.authenticate()
        # controller.signal(Signal.NEWNYM)
        # controller.set_options(({'ExitNodes': '{RU}'}))
        self.driver = webdriver.Chrome(executable_path=path, options=options)
        return self.driver

# driver = Webdriver().func_webdriver()
# def func_webdriver():  # todo переделать на класс, чтобы вызывая экземляр класса оставалась одна и та же сессия
#     options = Options()
#     path = os.getenv('chrome_driver')
#     mobile_emulation = {"deviceName": "Nexus 5"}
#     options.add_argument("--disable-notifications")
#     prefs = {"profile.managed_default_content_settings.images": 2}
#     options.add_experimental_option("prefs", prefs)
#     options.add_experimental_option("mobileEmulation", mobile_emulation)
#     # options.add_argument('--headless')
#     driver = webdriver.Chrome(executable_path=path, options=options)
#     return driver
#


