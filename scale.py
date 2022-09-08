import json


# skaliert alle Dateien, sodass sie zwischen 0 und 1 liegen
# -> es wird eine lineare Funktion erstellt, durch welche das Minimum bei 0 und das Maximum bei 1 ist
# in der Datei für ein Produkt, wird jeweils die Skalierung gespeichert
# als INPUT wird eine komplette Datei genommen, die bereits fertig klassifiziert wurde
def scale_data(sourcefile, targetfile):
    content = json.loads(open(sourcefile).read())

    for cat in content.keys():
        # Funktion berechnen, welche die Werte skalieren soll
        buffer = [content[cat][zeit] for zeit in content[cat].keys() if content[cat][zeit] is not None]
        max_x = max(buffer)
        min_x = min(buffer)
        m = 1/(max_x - min_x)  # Delta Y / Delta X
        n = 1 - (m * max_x)

        # alle Preise skalieren
        for zeit in content[cat].keys():
            if content[cat][zeit] is not None:
                content[cat][zeit] = (m * content[cat][zeit]) + n

        # Skalierung speichern
        content[cat].update({'scale': {'info': 'm = max_x - min_x, n = 1 - (m * max_x)', 'max_x': max_x, 'min_x': min_x}})
    open(targetfile, 'w', encoding='UTF-8').write(json.dumps(content))


scale_data('neuFiltern/Klassifiziert/PSU.json', 'Test.json')
