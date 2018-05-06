import os

MYDIR = os.path.dirname(__file__)
parentDir = os.path.dirname(MYDIR)
storageDir = os.path.join(parentDir, 'storage')
errorFile = os.path.join(storageDir, 'error.txt')
cogsDir = os.path.join(MYDIR, 'cogs')

dropboxPath = '/Mudhakkir'
