from pprint import pprint
import sys
import os
import json
from pprint import pprint


GPU = False
PSU = True
categories = {}
DATA = {}

if PSU:
    # 50 bis 1600 Watt sind möglich (32 * 50)
    for i in range(1, 33):
        categories.update({i * 50: []})
        DATA.update({i * 50: {}})
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
                            categories[c].append([file, data])
                except:
                    print('Problem bei: ' + file + f'!\n{data[1][0]} ist kein Integer!')
            else:
                print('WRONG FORMAT IN FILE: ' + file)

            for cat in categories.keys():
                if len(categories[cat]) != 0:
                    preisverlauf = {}
                    for product in categories[cat]:
                        for zeitpunkt in product[1][0].keys():
                            # falls der Zeitpunkt vorhanden ist und beide verfügbar sind
                            if zeitpunkt in preisverlauf.keys() and preisverlauf[zeitpunkt] is not None and product[1][0][zeitpunkt][0] is not None:
                                preisverlauf[zeitpunkt] = min(preisverlauf[zeitpunkt], product[1][0][zeitpunkt][0])
                            # falls der Zeitpunkt noch nicht vorhanden ist, oder TODO: das hier verstehen/fixen
                            elif zeitpunkt not in preisverlauf.keys() or product[1][0][zeitpunkt][0] is not None:
                                preisverlauf.update({zeitpunkt: product[1][0][zeitpunkt][0]})


for key in categories.keys():
    print(key, [categories[key][i][0] for i in range(len(categories[key]))])
