# reminder.py
from datetime import datetime, timedelta

class Reminder():

  def __init__(self):
    self.reminder_type = None
    self.reminder_id = []
    # If not repeat alarm deletes itself after going off
    self.repeat = False
    # Date building variables
    self.year = None
    self.month = None
    self.day = None
    self.hour = None
    self.minute = None
    # Delta variables
    self.in_days = 0
    self.in_hours = 0
    self.in_mins = 0
    # datetime string
    self.dt_string = None
    # Reminder list
    self.reminders = []

  def build(self):
    self.dt_string = self._format_string()

  def _format_string(self):
    now = datetime.now()
    if not self.year: self.year = now.year
    if not self.month: self.month = now.month
    if not self.day: self.day = now.day
    if not self.hour: self.hour = now.hour
    if not self.minute: self.minute = now.minute
    dt_obj = datetime(self.year, self.month, self.day, self.hour, self.minute)
    dt_obj = dt_obj + timedelta(
        days=self.in_days,
        hours=self.in_hours,
        minutes=self.in_mins)
    if dt_obj < datetime.now(): 
      dt_obj = dt_obj.replace(year=(dt_obj.year + 1))
    return dt_obj.strftime('%Y-%m-%d %H:%M')
