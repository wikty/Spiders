##
# selenium.webdriver module provides all the WebDriver implementations. 
# Currently supported WebDriver implementations are Firefox, Chrome, IE and Remote.
##
from selenium import webdriver
# webdriver.Firefox(
# firefox_profile=None, 
# firefox_binary=None, 
# timeout=30, 
# capabilities=None, 
# proxy=None, 
# executable_path='geckodriver', 
# firefox_options=None, 
# log_path='geckodriver.log')
# webdriver.FirefoxProfile
# webdriver.Chrome(
# executable_path='chromedriver', 
# port=0, 
# chrome_options=None, 
# service_args=None, 
# desired_capabilities=None, 
# service_log_path=None)
# webdriver.ChromeOptions
# webdriver.Ie
# webdriver.Opera
# webdriver.PhantomJS
# webdriver.Remote
# webdriver.DesiredCapabilities
# webdriver.ActionChains
# webdriver.TouchActions
# webdriver.Proxy


##
# Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
##
from selenium.webdriver.common.keys import Keys

# exceptions
# from selenium.common.exceptions import [TheNameOfTheExceptionClass]

##
# ActionChains are a way to automate low level interactions such as mouse movements, 
# mouse button actions, key press, and context menu interactions. 
# This is useful for doing more complex actions like hover over and drag and drop.
##
from selenium.webdriver.common.action_chains import ActionChains
# chain pattern

# menu = driver.find_element_by_css_selector(".nav")
# hidden_submenu = driver.find_element_by_css_selector(".nav #submenu1")
# ActionChains(driver).move_to_element(menu).click(hidden_submenu).perform()

# queue pattern
# menu = driver.find_element_by_css_selector(".nav")
# hidden_submenu = driver.find_element_by_css_selector(".nav #submenu1")
# actions = ActionChains(driver)
# actions.move_to_element(menu)
# actions.click(hidden_submenu)
# actions.perform()

##
# Use this class to interact with alert prompts. 
# It contains methods for dismissing, accepting, 
# inputting, and getting text from alert prompts.
##
from selenium.webdriver.common.alert import Alert

##
# utils
##
# selenium.webdriver.common.utils.find_connectable_ip
# selenium.webdriver.common.utils.free_port
# selenium.webdriver.common.utils.join_host_port
# selenium.webdriver.common.utils.keys_to_typing

##
# Color conversion support class
##
from selenium.webdriver.support.color import Color
# print(Color.from_string('#00ff33').rgba)
# print(Color.from_string('rgb(1, 255, 3)').hex)
# print(Color.from_string('blue').rgba)