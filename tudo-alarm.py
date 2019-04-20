# tudo-alarm.py
import os

HOME = os.path.expanduser('~')
ALARM_DIR = '/.local/share/tudo/alarms/'
PATH = HOME + ALARM_DIR

def check_alarms():
  for alarm_filename in os.listdir(PATH):
    parse_alarm(alarm_filename) 

def parse_alarm(alarm_filename):
  pass

if __name__ == '__main__':
  check_alarms()
