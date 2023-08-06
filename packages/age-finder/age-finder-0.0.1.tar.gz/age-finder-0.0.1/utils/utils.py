from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time as t
import os

def get_person(person: str):
	if not len(person) > 1:
		print("Please enter a name > 1 in length")
	else:
		person = person
	return person

def get_age(person: str):
	url = "https://www.google.com/search"
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--incognito")
	options.add_argument("--disable-extensions")
	options.add_argument("--disable-popup-blocking")
	driver = webdriver.Chrome(executable_path=r"/mnt/c/Users/613835631/tech_training/14_PyPi_Deployment/package_01/chromedriver/chromedriver.exe", options=options)
	driver.get(url)
	t.sleep(.2)
	cookie_button = driver.find_element_by_id("L2AGLb")
	cookie_button.click()
	t.sleep(.2)
	search_bar = driver.find_element_by_name("q")
	search_bar.clear()
	search_bar.send_keys(f"how old is {person}")
	search_bar.send_keys(Keys.ENTER)
	t.sleep(.2)
	age = driver.find_element_by_class_name("Z0LcW.XcVN5d").text
	driver.close()
	return age