import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import docx
from docx.shared import RGBColor
from docx.text.run import Font, Run

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
doc = docx.Document()
url = 'https://www.ldoceonline.com/browse/english/0-9/'
response = requests.get(url, headers=headers)

def getInnerData(a):
    response = requests.get(a, headers=headers)
    if response.status_code == 200:
        response = requests.get(a, headers=headers)
        html_soup_inner = BeautifulSoup(response.text, 'html.parser')
        title = HYPHENATION = PronCodes = POS = word_def = span = ''
        title = html_soup_inner.find('h1', class_=('pagetitle')).get_text()
        try:
            HYPHENATION = html_soup_inner.find('span', class_=('HYPHENATION')).get_text()
        except:
            pass
        try:
            PronCodes = html_soup_inner.find('span', class_=('PronCodes')).get_text()
        except:
            pass
        try:
            POS = html_soup_inner.find('span', class_=('POS')).get_text()
        except:
            pass
        word_def = html_soup_inner.find('span', class_=('DEF')).get_text()
        try:
            span = html_soup_inner.find('span', class_=('dictionary_intro','span')).get_text()
        except:
            pass
        doc.add_heading(title, 0)
        doc.add_heading(span, 5) if span != '' else ''
        hyp = doc.add_heading(HYPHENATION, 3) if HYPHENATION != '' else ''
        binary_run = hyp.add_run()
        binary_run.font.color.rgb =  RGBColor(255, 0, 0)
        doc.add_heading(PronCodes, 4) if PronCodes != '' else ''
        doc.add_heading(POS, 4) if POS != '' else ''
        doc.add_paragraph(word_def)
        doc.add_paragraph('\n\n')

def getDefs(a):
    response = requests.get(a, headers=headers)
    if response.status_code == 200:
        print('--', a)
        response = requests.get(a, headers=headers)
        html_soup_inner = BeautifulSoup(response.text, 'html.parser')
        try:
            title = HYPHENATION = PronCodes = POS = word_def = span = ''
            title = html_soup_inner.find('h1', class_=('pagetitle')).get_text()
            try:
                HYPHENATION = html_soup_inner.find('span', class_=('HYPHENATION')).get_text()
            except:
                pass
            try:
                PronCodes = html_soup_inner.find('span', class_=('PronCodes')).get_text()
            except:
                pass
            try:
                POS = html_soup_inner.find('span', class_=('POS')).get_text()
            except:
                pass
            word_def = html_soup_inner.find('span', class_=('DEF')).get_text()
            try:
                span = html_soup_inner.find('span', class_=('dictionary_intro','span')).get_text()
            except:
                pass
            doc.add_heading(title, 0)
            doc.add_heading(span, 5) if span != '' else ''
            doc.add_heading(HYPHENATION, 3) if HYPHENATION != '' else ''
            doc.add_heading(PronCodes, 4) if PronCodes != '' else ''
            doc.add_heading(POS, 4) if POS != '' else ''
            doc.add_paragraph(word_def)
            doc.add_paragraph('\n\n')
        except:
            a_list = ['https://www.ldoceonline.com' + x['href'] for x in html_soup_inner.find('span', class_=('ldoceEntry', 'Entry')).findAll('a')]
            print(a_list)
            words = []
            for a in a_list:
                getInnerData(a)

def getGroups(a, file_count):
    response = requests.get(a, headers=headers)
    if response.status_code == 200:
        html_soup_inner = BeautifulSoup(response.text, 'html.parser')
        a_list = ['https://www.ldoceonline.com' + x['href'] for x in html_soup_inner.find('ul', class_=('browse_results')).findAll('a')]
        for a in a_list:
            getDefs(a)



if response.status_code == 200:
    html_soup = BeautifulSoup(response.text, 'html.parser')
    a_list = ['https://www.ldoceonline.com' + x['href'] for x in html_soup.find('ul', class_=('browse_groups')).findAll('a')]
    print(a_list)
    file_count = 0
    for a in a_list:
        file_count += 1
        getGroups(a, file_count)
    doc.save('0-9.docx')
    