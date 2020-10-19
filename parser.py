from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Safari()
driver.get('https://fontawesome.com/icons?d=gallery&m=free')

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
    print(a_list)
    driver.quit()

with open('parser.html', 'w') as file:
    file.write(pageBody)