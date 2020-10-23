from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests

driver = webdriver.Safari()
driver.get('https://fontawesome.com/icons?d=gallery&m=free')

def findI(url, driver):
    driver.get(url)
    print(url)
    sleep(2)
    dwn = driver.find_element_by_class_name('fa-download')
    dwn.click()
    sleep(7)


try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a")))
    while True:
        try:
            btn = driver.find_element_by_class_name('mt3-ns')
            print('found')
            btn.click()
            print('ckicked')
            sleep(6)
        except:
            print('stop ckicking')
            break
    pageBody = driver.find_element_by_id('search-results').get_attribute('outerHTML')
    soup = BeautifulSoup(pageBody, 'html.parser')
    a_list = ['https://fontawesome.com' + x['href'] for x in soup.findAll('a')]
finally:
    a_list.pop(0)
    print('\n\n', len(a_list), '\n\n')
    for a in a_list:
        findI(a, driver)
    driver.quit()
