import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import config

username = '15620161152193'
password = '160318'

driver = webdriver.Firefox(executable_path=os.path.abspath(config.GECKODRIVER_PATH))
#  WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired)
driver.get("http://event.wisesoe.com/")
# find element by its name attribute
user_elem = driver.find_element_by_name("UserName")
user_elem.clear()
user_elem.send_keys(username)
pass_elem = driver.find_element_by_name('Password')
pass_elem.clear()
pass_elem.send_keys(password)
driver.find_element_by_class_name('click-logon').send_keys(Keys.RETURN) 

# control_elem = driver.find_element_by_id('default-menu-control')
# control_elem = control_elem.find_element_by_link_text('My reservations').click()

# select_elem = driver.find_element_by_id('ctl00_MainContent_termddl')
# select_elem = Select(select_elem)
# select_elem.select_by_value('2016-2017学年秋季学期')
# driver.close()