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


# import the necessary packages
import argparse
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
	help="name of the user")
ap.add_argument("-t", "--test", required=True,
	help="test")
args = vars(ap.parse_args())
# display a friendly message to the user
print("Hi there {}, it's nice to meet you!".format(args["name"]))

if args["test"] == "one":
    print("test arg =  {}".format(args["test"]))
