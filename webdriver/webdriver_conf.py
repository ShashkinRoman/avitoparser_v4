# -*- coding: utf-8 -*-
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome import service
from dotenv import load_dotenv
# from stem import Signal
# from stem.control import Controller
load_dotenv()


class Webdriver():

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

    def opera_driver(self):
        webdriver_service = service.Service('/home/roman/PycharmProjects/webriver/operadriver/operadriver')
        webdriver_service.start()

        opera_profile = r'/home/roman/.config/opera'
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=' + opera_profile)
        # options._binary_location = '/usr/lib/x86_64-linux-gnu/opera'
        self.driver = webdriver.Remote(webdriver_service.service_url,
                                       webdriver.DesiredCapabilities.OPERA, options=options)
        return self.driver

class Opera():
    webdriver_service = service.Service('/home/roman/PycharmProjects/webriver/operadriver/operadriver')
    webdriver_service.start()

    opera_profile = r'/home/roman/.config/opera'
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + opera_profile)
    # options._binary_location = '/usr/lib/x86_64-linux-gnu/opera'
    driver = webdriver.Remote(webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA, options=options)
