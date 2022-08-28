import os
import json
from pprint import pprint


GPU = False
PSU = True
categories = {}
data = {}

if PSU:
    # 50 bis 1600 Watt sind möglich (32 * 50)
    for i in range(1, 33):
        categories.update({i * 50: []})
        data.update({i * 50: {}})
path = 'Gefiltert/PSU/'


for file in os.listdir(path):
    if '._' not in file:
        data = json.loads(open(path + file, encoding='UTF-8').read())
        if PSU:
            if len(data[1].split()) == 2:  # alle rausfiltern die nicht im richtigen Format gespeichert wurden
                data[1] = data[1].split()
                try:
                    data[1][0] = int(data[1][0])
                    for c in categories.keys():
                        if data[1][0] in range(c - 50, c + 49):
                            categories[c].append(file)
                except:
                    print('Problem bei: ' + file + f'!\n{data[1][0]} ist kein Integer!')
            else:
                print('WRONG FORMAT IN FILE: ' + file)

            for wattage in categories.keys():



for key in categories.keys():
    print(key, categories[key])
