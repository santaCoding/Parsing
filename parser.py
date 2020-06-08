import requests
from bs4 import BeautifulSoup

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

def get_page(url):
    response = requests.get(url, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    ps = html_soup.findAll('p', class_='rtecenter')
    time = ''
    for p in range(len(ps)):
        time += ps[p].text + ' '
        if p%2 == 0 and p!= 0:
            print(time)
            time = ''

url = "http://ac.opu.ua/ru/priyomnaya-komissiya"
get_page(url)