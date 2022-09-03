import sys
from matplotlib import pyplot
import os
import json
from pprint import pprint


GPU = True
PSU = False
categories = {}
'''
Datenstruktur:
categories[wattage oder GPU_Chipset] = [alle GPUs/Netzteile zur category]
'''
DATA = {}
'''
Datenstruktur:
DATA[categorie] = {zeitpunkt: preis}
'''

if PSU:
    # 100 bis 1600 Watt sind möglich (16 * 100)
    for i in range(1, 17):
        categories.update({i * 100: []})
        DATA.update({i * 100: {}})
# path = 'test/'
path = 'Gefiltert/GPU/'


# die Produkte nach Kategorien sortieren
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
        if GPU:
            if data[1] not in categories.keys():
                if data[1] is not None:
                    categories.update({data[1]: [[file, data.copy()]]})
            else:
                categories[data[1]].append([[file, data.copy()]])


if PSU or GPU:
    for cat in categories.keys():
        if len(categories[cat]) != 0:
            preisverlauf = {}
            '''
            preisverlauf Datenstruktur:
            preisverlauf[zeitpunkt] = preis

            product Datenstruktur:
            liste[dateiname, dateiinhalt]
                dateiinhalt:
                liste[dict {preisdaten}, categorie]
                    preisdaten:
                        list[zeitpunkt] = [preis, shop]
            '''
            for product in categories[cat]:
                try:
                    for zeitpunkt in product[1][0].keys():
                        if zeitpunkt in preisverlauf.keys():  # Zeitpunkt ist bereits vorhanden
                            if preisverlauf[zeitpunkt] is None:  # war in dem Moment nicht verfügbar
                                preisverlauf[zeitpunkt] = product[1][0][zeitpunkt][0]
                            elif product[1][0][zeitpunkt][0] is not None:
                                if preisverlauf[zeitpunkt] > product[1][0][zeitpunkt][0]:  # war in dem Moment vorhanden, aber teurer
                                    preisverlauf[zeitpunkt] = product[1][0][zeitpunkt][0]
                        else:
                            preisverlauf.update({zeitpunkt: product[1][0][zeitpunkt][0]})
                except Exception as e:
                    print(e)
                    print(cat)
                    print(product)
                    sys.exit()
            DATA.update({cat: preisverlauf})


def visualize_data(xaxis, yaxis):
    pyplot.plot(xaxis)
    pyplot.ylabel(yaxis)
    pyplot.show()


# pprint(categories[500][0])

visualize_data([DATA['GeForce RTX 3080 10GB LHR'][zeitpunkt] for zeitpunkt in DATA['GeForce RTX 3080 10GB LHR'].keys()], [zeitpunkt for zeitpunkt in DATA['GeForce RTX 3080 10GB LHR'].keys()])
