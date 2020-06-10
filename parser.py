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
        heading = html_inner.find('h1', itemprop="name")
        print(heading.get_text())
        trs = html_inner.find('table', class_=('tbl_info', 'nf')).findAll('tr')
        #print(trs)
        tds = []
        for tr in trs:
            for td in tr.findAll('td', class_=None):
                if '\xa0' not in td:
                    tds.append(td.get_text().replace(' ', '').replace('\r', '').replace('Показать', ''))
        print('-'*20)
        print(tds)
        return heading.get_text(), tds

    else:
        print(f'error, not 200 for {url}')

def get_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        a_list = ['https://www.education.ua' + x['href'] for x in html_soup.findAll('a', class_=('viplink', 'h4_link'))]
        with open('text.csv', 'w', newline='') as csv_f:
            write = csv.writer(csv_f)
            write.writerow(('Название', 'Город', 'Год основания', 'Статус', 'Аккредитация', 'Документ об окончании', 'Форма обучения', 'Квалиф. уровни', 'Адрес', 'Телефон', 'Телефон приемное комиссии', 'Сайт'))
            for a in a_list:
                heading, data = get_inner_info(a)
                write.writerow((heading, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]))
    else:
        print('error, not 200')

url = "https://www.education.ua/universities/?city=32"
get_page(url)