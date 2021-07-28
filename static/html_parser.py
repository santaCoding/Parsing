from bs4 import BeautifulSoup
import pandas as pd
import numpy as np # changing 'None' pandas to '-' in pandas dataframe
import csv
import os

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
        house_info = house[0].find('b').text.split()   
        street = ''
        delete_count = 0
        first_part = house[0].find('b').text[:house[0].find('b').text.index(',')]
        second_part = house[0].find('b').text[house[0].find('b').text.index(',')+2:].split()
        
        if ') (' in house[0].find('b').text or first_part[-1] == ')':
            street = first_part[:first_part.index(')')+1]
            house_number = ''
            for symbol in range(len(first_part)-1, 0, -1):
                house_number = first_part[symbol] + house_number
                if first_part[symbol] == '(':
                    break
                try:
                    house_number = int(house_number)
                except:
                    pass
            zip = second_part[0] + ' ' + second_part[1]
            if len(zip) != 7:
                continue
            place = second_part[-1]
            add_number_info = None
        else:
            first_part = first_part.split()
            for word in first_part:
                word = word.replace(',', '')
                try:
                    int(word)
                    break
                except:
                    street += word + ' '
                    delete_count += 1
            street = street[:-1] #street
            del first_part[:delete_count]
            try:
                house_number = int(first_part[0]) #number
            except:
                continue
            try:
                house_number = int(house_number)
            except:
                pass
            first_part.pop(0)
            if len(first_part) != 0:
                add_number_info = ''
                for word in first_part:
                    add_number_info += word + ' '
                add_number_info = add_number_info[:-1] #add
            else:
                add_number_info = None

            zip = second_part[0] + ' ' + second_part[1] #zip
            if len(zip) != 7:
                continue
            place = ''
            second_part.pop(0)
            second_part.pop(0)

            for word in second_part:
                place += word + ' '
            place = place[:-1] #place



        title = {'House' : house[0].find('b').text,
                'Street_name' : street,
                'House_number' : house_number, 
                'House_number_addition' : add_number_info,
                'Zip-code' : zip,
                'Place' : place}

        print(f'{house_amount} house(s) collected from {len(houses)}')
        data = house[0].find_all('td', attrs={'style':'vertical-align:top; padding-left: 7px;'}) # first part of data
        innerdata = []
        for d in data:
            innerdata.append([str(x).strip() for x in d.contents if (str(x) != '<br/>' and str(x).strip() != '' and str(x).strip()[0] != "<")])
        innerdata[0][0] = 'Type_transaction: ' + innerdata[0][0]
        try:
            innerdata[0].insert(2, 'Price_type: ' + innerdata[0][1][innerdata[0][1].index(',')+3:])
            innerdata[0][1] = innerdata[0][1][:innerdata[0][1].index(',')]
        except:
            pass

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
        for data in range(len(innerdata)):
            if 'Adres' in innerdata[data].split()[0]:
                del_index = data
                main = innerdata[data][innerdata[data].index(':') + 2:].split()
                count = 0
                Street_makelaar = ''
                House_number_makelaar = 0
                House_number_addition_makelaar = ''
                while True:
                    try:
                        House_number_makelaar = int(main[count])
                        innerdata.insert(data+1, 'Street_makelaar: ' + Street_makelaar[:-1])
                        innerdata.insert(data+2, 'House_number_makelaar: ' + str(House_number_makelaar))
                        for c in range(0, count+1):
                            main.pop(0)
                        if len(main) > 0:
                            for elem in main:
                                House_number_addition_makelaar += elem + ' '
                            innerdata.insert(data+3, 'House_number_addition_makelaar: ' + House_number_addition_makelaar[:-1])
                        break
                    except:
                        Street_makelaar += main[count] + ' '
                    count += 1
        innerdata.pop(del_index)
        for data in range(len(innerdata)):
            if 'Plaats' in innerdata[data].split()[0]:
                del_index = data
                main = innerdata[data][innerdata[data].index(':') + 2:].split()
                Zip_code_makelaar = main[0] + ' ' + main[1]
                main.pop(0)
                main.pop(0)
                Plaats_makelaar = ''
                for elem in main:
                    Plaats_makelaar += elem + ' '
                innerdata.insert(data+1, 'Zip_code_makelaar: ' + Zip_code_makelaar)
                innerdata.insert(data+2, 'Plaats_makelaar: ' + Plaats_makelaar[:-1])
                break
        innerdata.pop(del_index)
        for data in range(len(innerdata)):
            if '€' in innerdata[data]:
                integer = ''
                for letter in range(len(innerdata[data])):
                    try:
                        if innerdata[data][letter] == ',' and innerdata[data][letter+1] != '-':
                            integer += '.'
                        else:
                            int(innerdata[data][letter])
                            integer += innerdata[data][letter]
                    except:
                        pass
                innerdata[data] = innerdata[data][:innerdata[data].index(':')+1] + ' ' + integer
            if 'Aanvaarding' in innerdata[data]:
                date = ''
                for letter in innerdata[data]:
                    try:
                        int(letter)
                        date += letter
                    except:
                        if letter == '-':
                            date += letter
                        else:
                            pass
                innerdata[data] = 'Aanvaarding: ' + date

        house_data1 = {}
        for data in innerdata:
            key = ''
            value = ''
            for d in range(len(data)):
                if data[d] != ':':
                    key+=data[d]
                else:
                    try:
                        value = int(data[d+2:])
                    except:
                        try:
                            value = float(data[d+2:])
                        except:
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
        
        if 'VvE_checklist_VvE bijdrage' in innerdata2[-1]:
            innerdata2.append('VvE_bijdrage_hoevaak: ' + innerdata2[-1][innerdata2[-1].index(',')+3:])
            innerdata2[-2] = innerdata2[-2][:innerdata2[-2].index(',')]

        numeric = ['Oppervlakten_en_inhoud',
                'Aantal badkamers',
                'Aantal woonlagen',
                'Bouwjaar',
                'Parkeercapaciteit',
                'Achtertuin', 
                'Buitenruimte',
                'Capaciteit',
                'Geen tuin']

        for data in range(len(innerdata2)):
            if 'Indeling_Aantal woonlagen' in innerdata2[data]:
                first = innerdata2[data][:innerdata2[data].index(':')]
                second = innerdata2[data][innerdata2[data].index(':')+2:].replace(' woonlaag', '').replace(' woonlagen', '')
                try:
                    int(second)
                    innerdata2[data] = first + ': ' + second
                except:
                    second = second.split()
                    value = second[0]
                    second.pop(0)
                    add = ''
                    for word in second:
                        add += word + ' '
                    innerdata2[data] = first + ': ' + value
                    innerdata2.insert(data+1, 'Aantal_woonlagen_extraerbij: ' + add[:-1])
            if 'Achtertuin' in innerdata2[data].split()[0] or 'Geen tuin' in innerdata2[data].split()[0] + ' ' + innerdata2[data].split()[1]:
                innerdata2[data] = innerdata2[data][:innerdata2[data].index('(')-4]
            if 'Aantal kamers' in innerdata2[data]:
                if '(' in innerdata2[data]:
                    innerdata2.insert(data+1, 'Indeling_Aantal_slaapkamers: ' + innerdata2[data][innerdata2[data].index('(')+1:len(innerdata2[data])-2].split()[0])
                    innerdata2[data] = 'Indeling_Aantal_kamers: ' + innerdata2[data][innerdata2[data].index(':')+2:].split()[0]
                else:
                    innerdata2[data] = 'Indeling_Aantal_kamers: ' + innerdata2[data][innerdata2[data].index(':')+2:].split()[0]

        
        for data in range(len(innerdata2)):
            for num in numeric:
                if num in innerdata2[data].split()[0]:
                    try:
                        int(innerdata2[data].split()[-1])
                    except:
                        temp = innerdata2[data].split()[:-1]
                        done = ''
                        for t in temp:
                            done += t + ' '
                        done = done[:-1]
                        innerdata2[data] = done
                    
        house_data2 = {}
        for data in innerdata2:
            key = ''
            value = ''
            for d in range(len(data)):
                if data[d] != ':':
                    key+=data[d]
                else:
                    try:
                        value = int(data[d+2:])
                    except:
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
    print(f'Your file is ready - \" {str(html_file).replace(".html", "")}.csv \"')
    file.close()
    return df

dfs = []
for root, dirs, files in os.walk("."):  
    for file in files:
        if 'html' in file[file.index('.'):]:
            dfs.append(parse_html(file))

dfs = pd.concat(dfs).sort_index()
dfs = dfs.replace(np.nan, '-')
print(dfs)