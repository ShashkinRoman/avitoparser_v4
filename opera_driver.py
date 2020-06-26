import time

from selenium import webdriver
from selenium.webdriver.chrome import service


webdriver_service = service.Service('/home/roman/PycharmProjects/webriver/operadriver/operadriver')
webdriver_service.start()

driver = webdriver.Remote(webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA)

driver.get('https://www.google.com/')
input_txt = driver.find_element_by_name('q')
input_txt.send_keys('operadriver\n')

time.sleep(5) #see the result
driver.quit()


from selenium import webdriver
from time import sleep
opera_profile = r'/home/roman/.config/opera'
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=' + opera_profile)
# options._binary_location = '/usr/lib/x86_64-linux-gnu/opera'
driver = webdriver.Opera(executable_path='/home/roman/PycharmProjects/webriver/operadriver/operadriver', options=options)
