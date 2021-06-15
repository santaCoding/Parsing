from bs4 import BeautifulSoup
import pandas as pd
import numpy as np # changing 'None' pandas to '-' in pandas dataframe
import csv

def parse_html(html_file):
    file = open(html_file, 'r', encoding='utf8')
    print('File opened')
    url = file.read()
    print('File read')
    print(f'Collecting data from {str(html_file)}, please wait...')
    soup = BeautifulSoup(url, 'lxml'    )
    print('Parsing all tables...')
    tables = soup.find_all('table') # collecting all <table> from html
    tables.pop(0) # delete extra
        
    print(f'Sorting {len(tables)} tables...')
    temp = []
    houses = []
    for table in range(len(tables)):
        if not temp and ('Verkocht' in tables[table].text or 'Verhuurd' in tables[table].text):
            temp.append(tables[table])
        elif len(temp) == 1 and 'Kenmerken' in tables[table].text:
            temp.append(tables[table])
        elif len(temp) == 2 and 'Aanbiedingstekst' in tables[table].text:
            temp.append(tables[table])
            houses.append(temp)
            temp = []
        try:
            if len(temp) == 2 and 'Aanbiedingstekst' not in tables[table+2].text and 'Aanbiedingstekst' not in tables[table+1].text:
                temp.append(None)
                houses.append(temp)
                temp = []
        except:
            pass
        
            
    house_data = []
    house_amount = 0
    for house in houses:
        house_amount += 1
        title = {'House' : house[0].find('b').text} # finding title of a house
        print(f'{house_amount} house(s) collected from {len(houses)}')
        data = house[0].find_all('td', attrs={'style':'vertical-align:top; padding-left: 7px;'}) # first part of data
        innerdata = []
        for d in data:
            innerdata.append([str(x).strip() for x in d.contents if (str(x) != '<br/>' and str(x).strip() != '' and str(x).strip()[0] != "<")])
        innerdata[0][0] = 'Type_transaction: ' + innerdata[0][0]
        num = ''
        prijsverloop_date = None
        if 'de markt' not in innerdata[0][-1]:
            prijsverloop_date = ''
            prijsverloop_date = innerdata[0][-1][len(innerdata[0][-1])-10:]
            delete_extra = 0
            date_index = 0
            while True:
                try:
                    if ':' not in innerdata[0][delete_extra] and 'op de markt' not in innerdata[0][delete_extra]:
                        innerdata[0].pop(delete_extra)
                    else:
                        delete_extra += 1
                except:
                    break
            for inner in range(len(innerdata[0])): #finding index of days_on_market variable
                if 'op de markt' in innerdata[0][inner]:
                    date_index = inner
            for inner in innerdata[0][date_index]: # finding digit in days on market
                if inner.isdigit():
                    num += inner
            innerdata[0].pop(date_index)
            innerdata[0].append('prijsverloop_date: ' + str(prijsverloop_date))
            innerdata[0].append('days_on_market: ' + num)
        else:
            for inner in innerdata[0][-1]: # finding digit in days on market
                if inner.isdigit():
                    num += inner
            innerdata[0].pop(len(innerdata[0])-1)
            innerdata[0].append('days_on_market: ' + num)
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
        spans = house[1].find_all('span') # second part of data
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


        try: 
            text = house[2].find_all('td')[1].contents # test house variable
            text = {'Text_house' : "\n".join([str(x) for x in text if str(x) != '<br/>'])}
        except:
            text = {'Text_house' : None}
            
            
        title.update(house_data1)
        title.update(house_data2)
        title.update(text)
        house_data.append(title) # house dict completed
        
    
            
    df = pd.DataFrame(house_data)
    df.index += 1
    df = df.replace(np.nan, '-')
    df.to_csv(f'{str(html_file).replace(".html", "")}.csv')
    print(df)
    print(f'Your file is ready - \" {str(html_file).replace(".html", "")}.csv \"')
    file.close()


parse_html('4536.html')