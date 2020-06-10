import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import csv

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

def get_inner_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_inner = BeautifulSoup(response.text, 'html.parser')
        heading = html_inner.find('h1', class_='heading')
        trs = html_inner.find('table', class_='w620').findAll('tr')
        print(trs)
        tds = []
        for tr in trs:
            for td in tr:
                tds.append(td)
        print('-'*20)
        print(tds)

    else:
        print(f'error, not 200 for {url}')

def get_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        a_list = ['https://www.education.ua' + x['href'] for x in html_soup.findAll('a', class_=('viplink', 'h4_link'))]
        get_inner_info
    else:
        print('error, not 200')

url = "https://www.education.ua/universities/?city=32"
get_page(url)