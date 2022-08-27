import os
import json

Netzteil = True
GPU = True


for datei in os.listdir('/Volumes/Hannes_USB/Gefiltert/PSU/'):
    datei = open('/Volumes/Hannes_USB/Gefiltert/PSU/' + datei, 'r', encoding='UTF-8').read()
    datei = json.loads(datei)

    if Netzteil:
        watt = datei[1]
        print(watt)
