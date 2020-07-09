import os
from selenium import webdriver
from selenium.webdriver.chrome import service
from dotenv import load_dotenv
load_dotenv()



webdriver_service = service.Service(os.getenv('opera_driver_path'))
webdriver_service.start()

path = (os.getenv('opera_profile_one'), os.getenv('opera_profile_two'), os.getenv('opera_profile_three'), os.getenv('opera_profile_four'), os.getenv('opera_profile_five'))


opera_profile = os.getenv('test_opera_driver')
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=' + opera_profile)
driver = webdriver.Remote(webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA, options=options)
# driver.get('https://whatismyipaddress.com')
# ip = driver.find_element_by_id('ipv4').text
# driver.close()


class Operadriver():

    def start_driver(self, path=os.getenv('opera_driver_path')):
        webdriver_service = service.Service(path)
        webdriver_service.start()
        return webdriver_service

    def opera(self, webdriver_service, opera_profile):
        # opera_profile = os.getenv('opera_driver')
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=' + opera_profile)
        # options._binary_location = '/usr/lib/x86_64-linux-gnu/opera'
        driver = webdriver.Remote(webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA, options=options)
        return driver

def driver(path):
    class_driver = Operadriver()
    start = class_driver.start_driver()
    driver = class_driver.opera(start, path)
    return driver

# class Opera_driver():
#     # def __init__(self):
#     #     self.driver = driver
#
#     def opera(self):
#         webdriver_service = service.Service('/home/roman/PycharmProjects/webdriver/operadriver/operadriver')
#         webdriver_service.start()
#
#         opera_profile = os.getenv('opera_driver')
#         options = webdriver.ChromeOptions()
#         options.add_argument('user-data-dir=' + opera_profile)
#         # options._binary_location = '/usr/lib/x86_64-linux-gnu/opera'
#         self.driver = webdriver.Remote(webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA, options=options)
#         return self.driver


