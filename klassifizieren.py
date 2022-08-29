from matplotlib import pyplot
import os
import json


GPU = False
PSU = True
categories = {}
DATA = {}
'''
Datenstruktur:
DATA[categorie] = {zeitpunkt: preis}
'''

if PSU:
    # 50 bis 1600 Watt sind möglich (32 * 50)
    for i in range(1, 33):
        categories.update({i * 50: []})
        DATA.update({i * 50: {}})
path = 'Gefiltert/PSU/'


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

if PSU:
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
                for zeitpunkt in product[1][0].keys():
                    if zeitpunkt in preisverlauf.keys():  # Zeitpunkt ist bereits vorhanden
                        if preisverlauf[zeitpunkt] is None:  # war in dem Moment nicht verfügbar
                            preisverlauf[zeitpunkt] = product[1][0][zeitpunkt][0]
                        elif product[1][0][zeitpunkt][0] is not None:
                            if preisverlauf[zeitpunkt] > product[1][0][zeitpunkt][0]:  # war in dem Moment vorhanden, aber teurer
                                preisverlauf[zeitpunkt] = product[1][0][zeitpunkt][0]
                    else:
                        preisverlauf.update({zeitpunkt: product[1][0][zeitpunkt][0]})
            DATA.update({cat: preisverlauf})


def visualize_data(xaxis, yaxis):
    pyplot.plot(xaxis)
    pyplot.ylabel(yaxis)
    pyplot.show()


cat = 500
maximum = [0, 0]
for zeit in DATA[cat].keys():
    if DATA[cat][zeit] is not None:
        if DATA[cat][zeit] > maximum[0]:
            maximum = [DATA[cat][zeit], zeit]

print(maximum)
visualize_data([DATA[cat][zeit] for zeit in DATA[cat].keys()], [zeit for zeit in DATA[cat].keys()])
