from selenium import webdriver
from selenium.webdriver.chrome import service

webdriver_service = service.Service('/home/user15/PycharmProjects/webdriver/operadriver/operadriver')
webdriver_service.start()

opera_profile = r'/home/user15/.config/opera'
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=' + opera_profile)
# options._binary_location = '/usr/lib/x86_64-linux-gnu/opera'
driver = webdriver.Remote(webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA, options=options)
driver.get('https://whatismyipaddress.com')
# ip = driver.find_element_by_id('ipv4').text
# driver.close()
