import json
import os
import sys
from pprint import pprint
from bs4 import BeautifulSoup
import datetime
import random
import time
from matplotlib import pyplot

testdaten = [{'data': [[34, 1329], [113, 328], [132, 775], [188, 287], [192, 234]], 'label': 'shop'},
             {'data': [[42, 206], [90, 1192], [134, 739], [175, 926], [187, 1842]], 'label': 'shop'}]


def stunde_runden(unixinput):
    return 3600000 * (unixinput // 3600000)


def get_preisdaten(file_path, withchipset, withwattage):
    extra = None  # eventuelle extra Daten zu dem Produkt (GPU Chipsatz/Netzteil Leistung)
    daten = {}
    '''
    Dateistruktur:
    Dictionary, Key = Zeitpunkt in Unixtime (Sekunden) -> darin ist Liste  Preis zu dem jeweiligen Zeitpunkt und dem jeweiligen Shoplabel
    '''
    file = open(file_path, encoding='UTF-8').read()
    Soup = BeautifulSoup(file, "html.parser")

    # gibt mehrere Male Script in dem HTML-DOc, das letzte enthält das gewollte Script hierfür mit den Daten
    wanted = Soup.find_all('script')[-1].text

    # nach allen einzelnen Befehlen von JS Splitten + den mit den Preisdaten raussuchen
    # (kann danach von JSON interpretiert werden)
    wanted = wanted.split(';')
    for element in wanted:
        if 'var chart_data' in element:
            wanted = element.split()[4:]  # falsche Klammern + Variablenennamen müssen entfernt werden

    buffer = wanted.copy()
    wanted = ''
    for element in buffer:
        wanted += element + ' '
    # jetzt ist in Wanted nurnoch die Zeile mit der Variable für die Preisdaten
    preisdaten = json.loads(wanted)
    if len(preisdaten) == 0:
        return None

    if withchipset:
        chipset = Soup.find_all('h2')
        for result in chipset:
            if 'Chipset' in result.text:
                extra = result.text.split(': ')[1]
                break

    if withwattage:
        chipset = Soup.find_all('p')
        for result in chipset:
            if 'W' in result.text:
                extra = result.text.strip()
                break
    '''
    Dateistruktur:
    Liste, in dieser sind die Preisdaten der einzelnen Shops vorhanden
    darin Dictionary mit den Keys label, data
    label -> enthält String mit der Shopbezeichnung
    data -> list mit den einzelnen Punkten für Preisdaten, 

    Element in dieser list:
    [zeit in unixtime (Millisekunden), Preis (Cent, wenn nicht verfügbar -> None)]
    '''

    # alle Daten auf einen Tag genau runden
    for zeitpunkt in range(stunde_runden(min([shop['data'][0][0] for shop in preisdaten])), stunde_runden(max([shop['data'][-1][0] for shop in preisdaten])), 3600000):
        # niedrigsten Preis zu diesem Zeitpunkt herausfinden
        preis = []  # enthält alle Shops mit den jeweligen Preisen, danach wird der mit dem Minimum ermittelt
        for shop in preisdaten:
            for datensatz in reversed(shop['data']):
                if stunde_runden(datensatz[0]) <= zeitpunkt + 3600000:
                    preis.append([datensatz[1], shop['label']])
                    break

        if len(daten.keys()) != 0:
            minpreis = [daten[zeitpunkt - 3600000][0], daten[zeitpunkt - 3600000][1]]
        else:
            minpreis = [None, None]
        for shop in preis:
            if minpreis[1] is shop[1]:  # wie sich der bisher günstigste Shop entwickelt hat
                minpreis = shop.copy()
            elif minpreis[0] is None and shop[0] is not None:  # wenn es jetzt verfügbar ist vorher aber nicht war
                minpreis = shop.copy()
            elif minpreis[0] is not None and shop[0] is not None:  # ob es jetzt einen günstigeren Shop gibt
                if minpreis[0] > shop[0]:
                    minpreis = shop.copy()
        daten.update({zeitpunkt: minpreis})
    return [daten, extra]


def filter_preisdaten(source_file, dest_file, GPU, PSU):
    data = get_preisdaten(source_file, GPU, PSU)
    if data is not None:
        open(dest_file, 'w').write(json.dumps(data))

begin = time.time()


counter = 0
files = os.listdir('/Volumes/Hannes_USB/Daten BWKI/PSU/')
for counter in range(0, len(files)):
    datei = files[counter]
    if datei[0] == '.':
        datei = datei[2:]
    try:
        filter_preisdaten('/Volumes/Hannes_USB/Daten BWKI/PSU/' + datei, '/Volumes/Hannes_USB/Gefiltert/PSU/' + datei.split('.')[0] + '.json', False, True)
    except:
        print('-------------------------------------------------------\n', datei, '\n----------------------------------------')
    if counter % 20 == 1:
        print('Zeit pro Datei', (time.time()-begin)/counter)
        print('geschätzte Prognose', ((time.time()-begin)/counter)*(len(os.listdir('/Volumes/Hannes_USB/Daten BWKI/PSU/'))-counter)/60)

print(time.time()-begin)
