import threading
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
from selenium.webdriver.support.ui import Select 
import os 
import datetime 
import sys 

from stem import Signal 
from stem.control import Controller 
from dotenv import load_dotenv

load_dotenv()

# Смена IP тора (9151 и 9150 - это для браузера тор, для сервера будет 9050 9051 соотвественно)
controller = Controller.from_port(port=9151)
controller.authenticate() 

options = webdriver.ChromeOptions() 
# options.add_argument('headless')
options.add_argument('--proxy-server=socks5://127.0.0.1:9150')

controller.signal(Signal.NEWNYM)
controller.set_options({
'ExitNodes':
	# '{US}, {CA},'
	' {RU}'
})
# mobile_emulation = {"deviceName": "Nexus 5"}
# # options.add_argument("--disable-notifications")
# prefs = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", prefs)
# options.add_experimental_option("mobileEmulation", mobile_emulation)
base_url = ("https://2ip.ru")

path = os.getenv('chrome_driver')
driver = webdriver.Chrome(executable_path=path, options=options)
driver.get(base_url)

def make_screenshot(index):
	controller.signal(Signal.NEWNYM)
	path = os.getenv('chrome_driver')
	driver = webdriver.Chrome(executable_path=path, options=options)
	driver.get(base_url) 
	driver.maximize_window() 
	#username = driver.find_element_by_id("Username") 
	#password = driver.find_element_by_id("Password") 
	#username.send_keys("username") 
	#password.send_keys("pass") 
	driver.save_screenshot(f"./landing_page{index}.png") 
	#driver.find_element_by_link_text('Logout').click() 
	 
	#driver.quit()

for i in range(2):
	threading.Thread(target=make_screenshot, args=(i,)).start()
	
controller.close()