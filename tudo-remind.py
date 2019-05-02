# tudo-alarm.py
from datetime import datetime
import os, threading, time

HOME = os.path.expanduser('~')
ALARM_DIR = '/.local/share/tudo/reminders/'
PATH = HOME + ALARM_DIR

class ReminderD():

  reminders = []
  num_reminders = 0 

  def start(self):
    while True:
      if self.count_reminders != self.num_reminders:
        self.check_reminders()
        self.num_reminders = self.count_reminders()
      time.sleep(60)

  def count_reminders(self):
    reminders = 0
    for f_name in os.listdir(PATH):
      if '.rmd' in f_name:
        reminders += 1
    return reminders

  def check_reminders(self):
    for f_name in os.listdir(PATH):
      if f_name not in self.reminders:
        if '.rmd' in f_name:
          self.reminders.append(f_name)
          print('reminder added: ' + f_name)
          parse_thread = threading.Thread(target=self.parse_reminder, args=[f_name])
          parse_thread.setDaemon(True)
          parse_thread.start()
        
  def parse_reminder(self, f_name):
    now = datetime.now()
    with open(PATH + f_name) as f:
      for line in f:
        line = line.rstrip('\n')
        line = line.split('.')    
        field = line[0]
        if field == 'dt_string':
          dt = datetime.strptime(line[1], '%Y-%m-%d %H:%M')  
          if now > dt:
            #execute reminder now
          else:
            time.sleep((dt-now).total_seconds())
            #Wait, then execute

if __name__ == '__main__':
  ReminderD().start()
