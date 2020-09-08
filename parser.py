import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
driver = webdriver.Safari()

driver.get('https://fontawesome.com/icons?d=gallery&m=free')

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a")))
    pageBody = driver.find_element_by_css_selector('body').get_attribute('outerHTML')
finally:
    driver.quit()

with open('parser.html', 'w') as file:
    file.write(pageBody)
