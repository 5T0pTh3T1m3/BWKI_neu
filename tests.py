import datetime
import json
import os

import requests
from pprint import pprint
from bs4 import BeautifulSoup


def get_product(prod_id):
    base_url = 'https://de.pcpartpicker.com/product/'
    return requests.request('GET', base_url + prod_id).text


def get_prod_ids(cat_id):
    pass


def get_cat_ids():
    # soup = BeautifulSoup(requests.request('GET', 'https://de.pcpartpicker.com/products/video-cards').text, 'html.parser')
    soup = BeautifulSoup(open('test.txt').read(), 'html.parser')
    lines = None
    for script in soup.find_all('script'):
        if 'datafilters' in script.text:
            lines = script.text.split('var')

    datafilters = None
    if lines is not None:
        for line in lines:
            if 'datafilters' in line:
                datafilters = line
                break

    if datafilters is not None:
        # datafilters = json.loads(datafilters)
        print(datafilters)


def format_timestamp(date):
    return int(datetime.datetime.timestamp(datetime.datetime.strptime(date.replace('-', ''), '%Y%m%d')) * 1000)


# liest den die Datei einer Kryptowährung ein, passt Format dem der anderen Daten an
def format_crypto_course(source_path, source_file, dest_path, dest_file):
    data = open(source_path + source_file).read().replace('\n', ',').split(',')
    formatted_data = [source_file.split('.')[0], {}]
    '''
    angestrebtes Format:
    list = [preisverlauf, währung]
        preisverlauf[zeitpunkt] = preis
    '''
    places = {'date': 0, 'close': 4}
    # bei 7 beginnen (erste Zeile sind die Attribute in plain), in 7 Schritten (allen Zeilen einzeln durchgehen)
    for i in range(7, len(data), 7):
        if data[i + places['date']] != '' and data[i + places['close']] != '':
            formatted_data[1].update({format_timestamp(data[i + places['date']]): data[i + places['close']]})
    open(dest_path + dest_file, 'w', encoding='UTF-8').write(json.dumps(formatted_data))
