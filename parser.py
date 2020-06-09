import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

def get_inner_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_inner = BeautifulSoup(response.text, 'html.parser')
        heading = html_inner.findAll('h1', class_='heading')
        vmiddle = html_inner.findAll('td', class_='vmiddle')
        tables = html_inner.findAll('table', class_='w620')
        return heading[0].get_text(), vmiddle[0].get_text(), tables[0].get_text()
    else:
        print(f'error, not 200 for {url}')

def get_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        trs = html_soup.findAll('tr', class_=('vip', 'odd', 'even'))
        a_list = []
        for tr in range(len(trs)):
            a_list.append('https://ru.osvita.ua' + trs[tr].a['href'])
        with open('text.csv', 'w') as csv_file:
            for page in a_list:
                heading_text, vmiddle_text, tables_text = get_inner_info(page)
                write = csv.writer(csv_file)
                write.writerow(heading_text)
                write.writerow(vmiddle_text)
                write.writerow(tables_text)
    else:
        print('error, not 200')

url = "https://ru.osvita.ua/vnz/guide/"
get_page(url)