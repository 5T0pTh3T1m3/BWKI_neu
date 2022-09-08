import json
from pprint import pprint

open('test/test1.json', 'w').write(json.dumps(json.loads(open('neuFiltern/Klassifiziert/CPU.json').read())['Intel Core i3-8300 3.7 GHz Quad-Core OEM/Tray Processor']))

