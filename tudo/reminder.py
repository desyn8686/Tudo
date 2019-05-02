# reminder.py
from datetime import datetime, timedelta
import os
import uuid

class Reminder():
  
  HOME = os.path.expanduser('~')
  REM_DIR = '/.local/share/tudo/reminders/'
  PATH = HOME + REM_DIR

  def __init__(self):
    self.name_hex = uuid.uuid4().hex
    self.reminder_type = None
    self.reminder_id = []
    # If not repeat alarm deletes itself after going off
    self.repeat = False
    self.repeat_days = 0
    self.repeat_hours = 0
    # Date building variables
    self.year = -1 
    self.month = -1
    self.day = -1
    self.hour = -1
    self.minute = -1
    # Delta variables
    self.in_days = 0
    self.in_hours = 0
    self.in_mins = 0
    # datetime string
    self.dt_string = None

  def build(self):
    self.dt_string = self._format_string()

  def _format_string(self):
    now = datetime.now()
    if self.year == -1: self.year = now.year
    if self.month == -1: self.month = now.month
    if self.day == -1: self.day = now.day
    if self.hour == -1: self.hour = now.hour
    if self.minute == -1: self.minute = now.minute
    dt_obj = datetime(self.year, self.month, self.day, self.hour, self.minute)
    dt_obj = dt_obj + timedelta(
        days=self.in_days,
        hours=self.in_hours,
        minutes=self.in_mins)
    if dt_obj < datetime.now(): 
      dt_obj = dt_obj.replace(year=(dt_obj.year + 1))
    return dt_obj.strftime('%Y-%m-%d %H:%M')

  def write(self):
    filename = self.PATH + self.name_hex + '.rmd'
    with open(filename, 'w', encoding='utf-8') as f:
      f.write('dt_string.' + self.dt_string + '\n')
      f.write('type.' + self.reminder_type + '\n')
      first = True
      f.write('idlist.')
      for item_id in self.reminder_id:
        if first == False:
          f.write('.')
        f.write(item_id)
        first = False
      f.write('\n')
      f.write('repeat.' + str(self.repeat) + '\n')
      if self.repeat:
        f.write('rdays.' + str(self.repeat_days) + '\n')
        f.write('rhours.' + str(self.repeat_hours) + '\n')
