import os


gitignore = open('.gitignore', 'a')
path_to_ignore = 'neuFiltern/'
for file in os.listdir(path_to_ignore):
    gitignore.write('\n' + path_to_ignore + file)
gitignore.close()
