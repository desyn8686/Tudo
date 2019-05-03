# tudo-alarm.py
from datetime import datetime, timedelta
from tudo.reminder import Reminder
import tudo.tlist_io as tlist_io
import os, threading, time
import smtplib
import getpass

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
          self.reminders.append(f_name.rstrip('.rmd'))
          parse_thread = threading.Thread(target=self.parse, args=[f_name])
          parse_thread.setDaemon(True)
          parse_thread.start()
        
  def parse(self, f_name):
    reminder_data = {}
    with open(PATH + f_name) as f:
      for line in f:
        line = line.rstrip('\n')
        line = line.split('.')    
        field = line[0]
        reminder_data[field] = line[1:len(line)]
        if len(reminder_data[field]) == 1 and field != 'idlist':
          reminder_data[field] = reminder_data[field][0]
    self.schedule_reminder(reminder_data)

  def schedule_reminder(self, data_dict):
    task_list = self.fetch_tasks(data_dict['type'], data_dict['idlist'])
    greeting = self.build_greeting(data_dict['type'])
    message = self.build_message(task_list)

    now = datetime.now()
    reminder_dt = datetime.strptime(data_dict['dt_string'], '%Y-%m-%d %H:%M')
    if now > reminder_dt:
      self.send(greeting + '\n' + message)
    else:
      delay = reminder_dt - now
      delay_seconds = delay.total_seconds()
      time.sleep(delay_seconds)
      self.send(greeting + '\n' + message)
    self.cleanup(data_dict)

  def fetch_tasks(self, rtype, id_list):
    tasks = []
    if rtype == 'task':
      list_id = id_list[0]
      task_id = id_list[1]
      tlist_data = tlist_io.parse_list(list_id + '.tlist')
      list_tasks = {'name': tlist_data['name'], 'group': tlist_data['group'], 'tasks': []}
      for task_dict in tlist_data['tasks']:
        if task_dict['id'] == task_id:
          task = {}
          task['tag'] = task_dict['tag'].lstrip('o').lstrip('x')
          task['expan'] = []
          for expan_line in task_dict['expan']:
            if expan_line[0] == 'o':
              task['expan'].append(expan_line.lstrip('o'))
          list_tasks['tasks'].append(task)
      tasks.append(list_tasks)
    elif rtype == 'list':
      list_id = id_list[0]
      tlist_data = tlist_io.parse_list(list_id + '.tlist')
      list_tasks = {'name': tlist_data['name'], 'group': tlist_data['group'], 'tasks': []}
      for task_dict in tlist_data['tasks']:
        if task_dict['tag'][0] == 'o':
          task = {}
          task['tag'] = task_dict['tag'].lstrip('o').lstrip('x')
          task['expan'] = []
          for expan_line in task_dict['expan']:
            if expan_line[0] == 'o':
              task['expan'].append(expan_line.lstrip('o'))
          list_tasks['tasks'].append(task)
      tasks.append(list_tasks)
    elif rtype == 'group':
      for list_id in id_list:
        tlist_data = tlist_io.parse_list(list_id + '.tlist')
        list_tasks = {'name': tlist_data['name'], 'group': tlist_data['group'], 'tasks': []}
        for task_dict in tlist_data['tasks']:
          if task_dict['tag'][0] == 'o':
            task = {}
            task['tag'] = task_dict['tag'].lstrip('o').lstrip('x')
            task['expan'] = []
            for expan_line in task_dict['expan']:
              if expan_line[0] == 'o':
                task['expan'].append(expan_line.lstrip('o'))
            list_tasks['tasks'].append(task)
        tasks.append(list_tasks)
    return tasks
    
  def build_greeting(self, rtype):
    greeting = 'Hello!\n'
    greeting = greeting + 'This is a reminder from Tudo!\n'
    greeting = greeting + 'You wanted to be reminded about this '
    if rtype != 'group':
      greeting = greeting + rtype + ':\n'
    else:
      greeting = greeting + rtype + ' of lists:\n'
    return greeting

  def build_message(self, task_list):
    message = ''
    for tlist in task_list:
      message = message + '--------------------\n\n'
      message = message + ' List: ' + tlist['name'] + '\n'
      message = message + 'Group: ' + tlist['group'] + '\n\n'
      message = message + 'Tasks:\n'
      i = 1
      for task in tlist['tasks']:
        if len(tlist['tasks']) == 1:
          message = message + '> ' + task['tag'] + '\n'
        else:
          message = message + str(i) + ' ' + task['tag'] + '\n'
        i += 1
        for expan in task['expan']:
          message = message + '  -' + expan + '\n'
      message = message + '\n'
    return(message)

  def send(self, reminder): 
    SERVER = 'localhost'
    FROM = 'tudo'
    TO = [getpass.getuser()]

    SUBJECT = 'A REMINDER!'
    TEXT = reminder

    message = '''\
From: %s
To: %s
Subject: %s

%s
''' %(FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()

  def cleanup(self, data_dict):
    if data_dict['repeat'] == 'True': 
      now = datetime.now()
      dt_obj = datetime.strptime(data_dict['dt_string'])
      while now > dt_obj:
        dt_obj = dt_obj + timedelta(days=int(data_dict['rdays']), hours=int(data_dict['rhours']))
      data_dict['dt_string'] = dt_obj.strftime('%Y-%m-%d %H:%M')
      reminder = Reminder()
      reminder.name_hex = data_dict['hex']
      reminder.reminder_type = data_dict['type']
      for rid in data_dict['idlist']:
        reminder.reminder_id.append(rid)
      reminder.repeat = True
      reminder.repeat_days = data_dict['rdays']
      reminder.repeat_hours = data_dict['rhours']
      reminder.dt_string = data_dict['dt_string']
      reminder.write()
      self.reminders.remove(data_dict['hex'])
      self.check_reminders()
    else:
      self.reminders.remove(data_dict['hex'])
      if os.path.exists(PATH + data_dict['hex'] + '.rmd'):
        os.remove(PATH + data_dict['hex'] + '.rmd')

if __name__ == '__main__':
  ReminderD().start()
