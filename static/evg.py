from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
from time import sleep
import pdb
#pdb.set_trace()

with open('4.html', 'r') as file:
    print('File opened\nWaiting 10 secs...')
    sleep(2)
    url = file.read()
    print('File read\nWaiting 10 secs...')
    sleep(2)
    soup = BeautifulSoup(url, 'html.parser')
    print('Parsing all tables...')
    tables = soup.find_all('table')
    tables.pop(0)
    table_count = 2
    print(f'Collecting {len(tables)} tables...')
    while True:
        try:
            tables.pop(table_count)
            table_count+=3
        except:
            break
    houses = []
    
    print(f'Sorting {len(tables)} tables...')
    while True:
        temp = []
        try:
            for table in range(0, 3):
                temp.append(tables[table])
            del tables[:3]
            houses.append(temp)
        except:
            break
    
        
    house_data = []
    house_amount = 0
    for house in houses:
        house_amount += 1
        title = {'House' : house[0].find('b').text}
        print(f'{house_amount} house(s) collected from {len(houses)}')
        data = house[0].find_all('td', attrs={'style':'vertical-align:top; padding-left: 7px;'})
        innerdata = []
        for d in data:
            innerdata.append([str(x).strip() for x in d.contents if (str(x) != '<br/>' and str(x).strip() != '' and str(x).strip()[0] != "<")])
        innerdata[0][0] = 'Type_transaction: ' + innerdata[0][0]
        num = ''
        for inner in innerdata[0][-1]:
            if inner.isdigit():
                num += inner
        innerdata[0][-1] = 'days_on_market: ' + num
        innerdata.pop(1)
        innerdata = innerdata[0] + innerdata[1]
        house_data1 = {}
        for data in innerdata:
            key = ''
            value = ''
            for d in range(len(data)):
                if data[d] != ':':
                    key+=data[d]
                else:
                    value = data[d+2:]
                    break
            house_data1.update({key:value})
            

                #--------------

        
        innerdata2 = []
        tds = house[1].find_all('td')
        spans = house[1].find_all('span')
        i = -1
        tds.pop(0)
        for td in tds:
            del td[:-1]
            td = [str(t).strip() for t in td if str(t) != '<br/>' and str(t).strip() != '']
            for t in range(len(td)):
                if td[t][0] == '<':
                    if t != len(td)-1 and td[t+1] == '<':
                        innerdata2.append(spans[i].text.replace(' ', '_') + ' -')
                    else:
                        i+=1
                else:
                    td[t] = spans[i].text.replace(' ', '_') + '_' + td[t]
                    innerdata2.append(td[t])

        house_data2 = {}
        for data in innerdata2:
            key = ''
            value = ''
            for d in range(len(data)):
                if data[d] != ':':
                    key+=data[d]
                else:
                    value = data[d+2:]
                    break
            house_data2.update({key:value})


        
        text = house[2].find_all('td')[1].contents
        text = {'Text_house' : "\n".join([str(x) for x in text if str(x) != '<br/>'])}
        
        
        title.update(house_data1)
        title.update(house_data2)
        title.update(text)
        house_data.append(title)
        
        
        
    df = pd.DataFrame(house_data)
    df.index += 1
    df = df.replace(np.nan, '-')
    df.to_csv('load.csv')
    print(df)
        