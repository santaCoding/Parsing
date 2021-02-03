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
    dhtml = driver.find_element_by_css_selector('body').get_attribute('outerHTML')
    btn = driver.find_element_by_css_selector('li.order-8-l.gray5')
    btn.click()
    dwn = driver.find_element_by_css_selector('div.ph5.pv4.bg-gray1.br3.br--bottom')
    dwn.click()
    sleep(3)


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
    a_list = a_list[1011:]
    print('\n\n', len(a_list), '\n\n')
    for a in range(len(a_list)):
        print(a+1)
        findI(a_list[a], driver)
    driver.quit()
