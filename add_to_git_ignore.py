import os


gitignore = open('.idea/.gitignore', 'a')
for file in os.listdir('neuFiltern/GPU/'):
    gitignore.write('\nneuFiltern/GPU/' + file)
gitignore.close()
