import os
import json

Netzteil = True
GPU = True


for datei in os.listdir('/Volumes/Hannes_USB/Gefiltert/PSU/'):
    if datei[0] == '.':
        datei = datei[2:]
    datei = open('/Volumes/Hannes_USB/Gefiltert/PSU/' + datei, 'r', encoding='UTF-8').read()
    datei = json.loads(datei)

    if Netzteil:
        watt = datei[1].split(' W')[0]
        try:
            watt = int(watt)

            liste = os.listdir
            liste[len(liste)-1] = liste[len(liste)-1][2:]

            if str(watt) + '.json' in liste:
                for time_stamp in datei[0].keys():
                    datei[0][time_stamp]
            else:
                datei2 = open('/Volumes/Hannes_USB/Final/PSU/' + str(watt), 'a')
                datei2.write(datei[0])
                datei2.close()

        except:
            print('fehlerhafte Datei:', datei)

