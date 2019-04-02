# tlist.py
from urwid import WidgetWrap, SimpleFocusListWalker, ListBox, Text, AttrSpec, AttrMap, Filler, Frame, LineBox
from task import Task
import uuid


class TList(WidgetWrap):

  def __init__(self, list_data=None):

    self.is_editing = False

    self.tasks = []
    self.name = ''
    self.id = ''

    if list_data: 
      # Parse the data.
      self.parse_data(list_data)
    else:
      # Must be a new list
      self.name = 'untitled'
      self.id = uuid.uuid4().hex

    # Build widget stack
    self.title = self.build_title()
    self.body = SimpleFocusListWalker(self.tasks)
    self.list_box = ListBox(self.body)
    self.list_frame = Frame(self.list_box, header=self.title)
    self.line_box = LineBox(self.list_frame)
    self.line_attr = AttrMap(self.line_box, AttrSpec('', ''), AttrSpec('h12', ''))
    super().__init__(self.line_attr)

  def build_title(self):
    title_text = Text((AttrSpec('black', 'light gray'), ' ' + self.name + ' '), align='center')
    title_map = AttrMap(title_text, AttrSpec('', 'black'))
    return title_map 

  def parse_data(self, list_data):

    self.name = list_data['name']
    task_data = list_data['tasks']

    index = 1
    for task_dict in task_data:
      task = Task(index, task_dict)
      index += 1
      self.tasks.append(task)

  def _write_buffer(self, task_data, data_buffer):
    task_data.append(data_buffer.copy())
    data_buffer.clear()

  def export(self):
    data = {'name': self.name, 'id': self.id, 'tasks': []}
    for task in self.tasks:
      task_dict = {} 
      task_dict['tag'] = task.tag.get_text()
      task_dict['expan'] = task.expan.get_lines()
      data['tasks'].append(task_dict)

    return data

  def keypress(self, size, key):
    if not self.is_editing: 
      if key == 'i':
        self.is_editing = True
      elif key == 'j':
        self.move_focus(1)
      elif key == 'k':
        self.move_focus(-1)
      elif key == 'e':
        self.list_box.focus.toggle_expan()
      elif key == 'h':
        self.list_box.focus.move_cursor(-1)
      elif key == 'l':
        self.list_box.focus.move_cursor(1)
      elif key == 'x':
        self.list_box.focus.toggle_strike()
      else:


        return key
    elif key == 'esc' and self.is_editing:
      self.is_editing = False
      pass
    elif self.is_editing: return super().keypress(size, key)

  def redraw(self):
    pass

  def move_focus(self, trans):
    focus_task = self.list_box.focus
    sub_focus = focus_task.task_pile.focus
    if sub_focus == focus_task.expan:
      try:
        sub_focus.expan_pile.focus_position += trans
      except IndexError:
        try:
          focus_task.task_pile.focus_position += trans
        except IndexError:
          try:
            self.list_box.focus_position += trans
          except IndexError:
            pass
    else:
      try:
        focus_task.task_pile.focus_position += trans
      except IndexError:
        try:
          self.list_box.focus_position += trans
        except IndexError:
          pass
