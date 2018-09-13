# Python language bindings for Selenium WebDriver
# https://pypi.python.org/pypi/selenium
from selenium.webdriver.phantomjs.webdriver import WebDriver

dirver = WebDriver(executable_path="../example/phantomjs-2.1.1-windows/bin/phantomjs.exe")
dirver.get('http://www.baidu.com')
print(dirver.title)