import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

def get_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        trs = html_soup.findAll('tr', class_=('vip', 'odd', 'even'))
        a_list = []
        for tr in range(len(trs)):
            a_list.append('https://ru.osvita.ua' + trs[tr].a['href'])
        print(a_list)
        for page in a_list:
            response = requests.get(page)
            print(response.status_code)
            sleep(randint(1,2))
    else:
        print('error, not 200')

url = "https://ru.osvita.ua/vnz/guide/"
get_page(url)