# tudo-install.py
import os

HOME = os.path.expanduser('~')
BASE_DIR = HOME + '/.local/share/tudo/'

LIST_PATH = BASE_DIR + 'lists/'
ALARM_PATH = BASE_DIR + 'reminders/'

INSTALL_DIRS = [LIST_PATH,
        ALARM_PATH]

def install():
  create_dirs()

def create_dirs():
  for DIR in INSTALL_DIRS:
    try:
      os.makedirs(DIR)
    except FileExistsError:    
      print('Errors: %s: dir already exists' %(DIR))

if __name__ == '__main__':
  install()
