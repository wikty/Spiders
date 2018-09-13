import os

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

import config
print(os.path.abspath(config.PHANTOMJS_PATH))
driver = webdriver.PhantomJS(executable_path=os.path.abspath(config.PHANTOMJS_PATH))
#  WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired)
driver.get("http://www.python.org")
assert "Python" in driver.title
# find element by its class name
elem = driver.find_element_by_class_name('slide-code').find_element_by_tag_name('code')
elem.screenshot('test.png')
# The quit will exit entire browser whereas close` will close one tab, but if just one tab was open
# driver.quit()
# driver.close()