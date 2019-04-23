# tlist_io.py
from tudo.tlist import TList
import os
import uuid

# List declaration
LIST_OP = '@'
# Hex declaration 
HEX_OP = '#'
# Group declaration
GROUP_OP = '^'
# Task declaration
TASK_OP = '!'
# Task ID
TASK_ID = '$'
# Expan declaration
EXPAN_OP = '-'

HOME = os.path.expanduser('~')
LIST_DIR = '/.local/share/tudo/lists/'
PATH = HOME + LIST_DIR

def load_list_data():

  loaded_lists = []
  for tlist_filename in os.listdir(PATH):
    tlist_data = parse_list(tlist_filename)
    loaded_lists.append(tlist_data)

  return loaded_lists

def parse_list(filename):

  tlist_data = { 'name': '', 'id': '', 'group': '', 'tasks': []} 
  data_buffer = {}
  
  with open(PATH + filename) as f:
    for line in f:
      # Format line 
      op_char = line[0]
      line = line.lstrip(op_char)
      line = line.rstrip('\n')

      if op_char == LIST_OP: 
        tlist_data['name'] = line
      elif op_char == HEX_OP:
        tlist_data['id'] = line
      elif op_char == GROUP_OP:
        tlist_data['group'] = line
      elif op_char == TASK_ID:
        if data_buffer: _write_buffer(tlist_data['tasks'], data_buffer)
        if line == 'NONE': line = uuid.uuid4().hex
        data_buffer['id'] = line
        data_buffer['expan'] = []
      elif op_char == TASK_OP:
        data_buffer['tag'] = line
      elif op_char == EXPAN_OP:
        data_buffer['expan'].append(line)

  if data_buffer: _write_buffer(tlist_data['tasks'], data_buffer)
  return tlist_data

def _write_buffer(task_data, data_buffer):
  task_data.append(data_buffer.copy())
  data_buffer.clear()

def save_all(data_tuple):
  tlists = data_tuple[0]
  deleted = data_tuple[1]
  print('Saving all lists:')
  for tlist_id in deleted:
    print('  Deleting: ID: ' + tlist_id)
    delete_list(tlist_id)
  for data_dict in tlists:
    print('  Saving: ID: ' + data_dict['id'])
    save_list(data_dict)

def save_list(tlist_data):
  filename = PATH + tlist_data['id'] + '.tlist'
  with open(filename, 'w') as f:
    f.write(LIST_OP + tlist_data['name'] + '\n')
    f.write(GROUP_OP + tlist_data['group'] + '\n')
    f.write(HEX_OP + tlist_data['id'] + '\n')
    for task in tlist_data['tasks']:
      f.write(TASK_ID + task['id'] + '\n')
      f.write(TASK_OP + task['tag'] + '\n')
      for line in task['expan']:
        f.write(EXPAN_OP + line + '\n')

def delete_list(tlist_id):
  filename = PATH + tlist_id + '.tlist'
  try:
    os.remove(filename)
  except FileNotFoundError:
    pass
