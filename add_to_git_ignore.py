import os


gitignore = open('.idea/.gitignore', 'a')
for file in os.listdir('gefiltert/CPU/'):
    gitignore.write('\ngefiltert/CPU/' + file)
gitignore.close()
