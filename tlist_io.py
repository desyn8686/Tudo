# tlist_io.py
from tlist import TList

# List declaration
LIST_OP = '@'
# Hex declaration 
HEX_OP = '#'
# Group declaration
GROUP_OP = '^'
# Task declaration
TASK_OP = '!'
# Expan declaration
EXPAN_OP = '-'

def load_list(filename):

  tlist_data = { 'name': '', 'id': '', 'tasks': []} 
  data_buffer = {}
  
  with open(filename) as f:
    for line in f:
      # Format line 
      op_char = line[0]
      line = line.lstrip(op_char)
      line = line.rstrip('\n')

      # Why doesn't python have a case statement?
      if op_char == LIST_OP: 
        tlist_data['name'] = line
      elif op_char == HEX_OP:
        tlist_data['id'] = line
      elif op_char == GROUP_OP:
        tlist_data['group'] = line
      elif op_char == TASK_OP:
        if data_buffer: _write_buffer(tlist_data['tasks'], data_buffer)
        data_buffer['tag'] = line
        data_buffer['expan'] = []
      elif op_char == EXPAN_OP:
        data_buffer['expan'].append(line)

  if data_buffer: _write_buffer(tlist_data['tasks'], data_buffer)

  return tlist_data

def _write_buffer( task_data, data_buffer):
  task_data.append(data_buffer.copy())
  data_buffer.clear()

def save_list(tlist_data):
  filename = '/home/desyn8686/Tudo/.lists/' + tlist_data['id'] + '.tlist'
  with open(filename, 'w') as f:
    f.write(LIST_OP + tlist_data['name'] + '\n')
    f.write(HEX_OP + tlist_data['id'] + '\n')
    for task in tlist_data['tasks']:
      f.write(TASK_OP + task['tag'] + '\n')
      for line in task['expan']:
        f.write(EXPAN_OP + line + '\n')
