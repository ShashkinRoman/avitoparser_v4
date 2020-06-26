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