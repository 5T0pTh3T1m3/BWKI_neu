import json


def format_file(sourcefile):
    content = json.loads(open(sourcefile).read())

    bezeichnungen = []
    zeiten = []
    preise = []
    skalierungen = []

    for product in content.keys():
        bezeichnungen.append(product)

        for zeitpunkt in content[product].keys():

