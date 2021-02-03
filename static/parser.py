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
        tds = []
        for tr in trs:
            for td in tr.findAll('td', class_=None):
                if '\xa0' not in td:
                    tds.append(td.get_text().replace(' ', '').replace('\r', '').replace('Показать', ''))
        print('-'*20)
        if len(tds) == 11:
            tds.pop(9)
        return heading.get_text(), tds

    else:
        print(f'error, not 200 for {url}')

def get_page(url, counter):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        a_list = ['https://www.education.ua' + x['href'] for x in html_soup.findAll('a', class_=('viplink', 'h4_link'))]
        with open('odessas_unives.csv', 'a', newline='') as csv_f:
            write = csv.writer(csv_f)
            for a in a_list:
                heading, data = get_inner_info(a)
                write.writerow((counter, heading, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]))
                counter += 1
        return counter
    else:
        print('error, not 200')
        return counter

with open('odessas_unives.csv', 'w') as csv_f:
    write = csv.writer(csv_f)
    write.writerow(('№', 'Title', 'City', 'Year of founding', 'Status', 'Accreditation', 'Ending document', 'Educational form', 'Qualification levels', 'Adress', 'Telephone', 'Website'))
counter = 1
url = "https://www.education.ua/universities/?city=32"
counter = get_page(url, counter)
url = 'https://www.education.ua/universities/?page=2&city=32&desc=1'
counter = get_page(url, counter)
