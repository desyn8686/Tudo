# tlist.py
from urwid import WidgetWrap, SimpleFocusListWalker, ListBox, Edit, AttrSpec, AttrMap, Filler, Frame, LineBox
from task import Task
from title_bar import TitleBar
from group_foot import GroupFoot
import uuid


class TList(WidgetWrap):

  def __init__(self, list_data=None):

    self.is_editing = False

    self.tasks = []
    self.name = None
    self.group = None
    self.id = None

    if list_data: 
      # Parse the data.
      self.parse_data(list_data)
    else:
      # Must be a new list
      self.name = 'untitled'
      self.group = 'none'
      self.id = uuid.uuid4().hex

    # Build widget stack
    self.title = TitleBar(self.name)
    self.group_foot = GroupFoot(self.group)
    self.body = SimpleFocusListWalker(self.tasks)
    self.list_box = ListBox(self.body)
    self.list_frame = Frame(self.list_box, header=self.title, footer=self.group_foot)
    self.line_box = LineBox(self.list_frame)
    self.line_attr = AttrMap(self.line_box, AttrSpec('', ''), AttrSpec('h12', ''))
    super().__init__(self.line_attr)

  def parse_data(self, list_data):

    self.name = list_data['name']
    self.group = list_data['group']
    self.id = list_data['id']
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
    data = {'name': self.name, 'group': self.group, 'id': self.id, 'tasks': []}
    for task in self.tasks:
      task_dict = {} 
      if task.tag.strikethrough:
        task_dict['tag'] = 'x' + task.tag.get_text()
      else:
        task_dict['tag'] = 'o' + task.tag.get_text()
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
        try:
          self.list_box.focus.toggle_expan()
        except AttributeError:
          pass
      elif key == 'h':
        try:
          self.list_box.focus.move_cursor(-1)
        except AttributeError:
          pass
      elif key == 'l':
        try:
          self.list_box.focus.move_cursor(1)
        except AttributeError:
          pass
      elif key == 'x':
        try:
          self.list_box.focus.toggle_strike()
        except AttributeError:
          pass
      elif key == 'n':
        self.list_frame.focus_position = 'header' 
        self.is_editing = True
      elif key == 'g':
        self.list_frame.focus_position = 'footer'
        self.is_editing = True
      elif key == 'd':
        if self.list_box.focus:
          if self.list_box.focus.pile.focus_position == 0:
            return 'delete task', self
          else:
            return 'delete expan', self.list_box.focus
      elif key == 'T':
        new_task = Task()
        self.tasks.append(new_task)
        self.body.append(new_task)
        self.index_tasks()
      elif key == 't':
        if self.list_box.focus:
          focus = self.list_box.focus
          focus.expan.new()
          focus.show_expan = True
          focus.redraw_expan()
        
      else:
        return key

    elif (key == 'esc' or key == 'enter') and self.is_editing:
      self.is_editing = False
      if self.list_frame.focus_position != 'body':
        self.name = self.title.edit.edit_text
        self.group = self.group_foot.edit.edit_text
        self.list_frame.focus_position = 'body'
      pass
    elif self.is_editing: return super().keypress(size, key)

  def delete_focus(self):
    self.tasks.remove(self.list_box.focus)
    self.body.remove(self.list_box.focus)
    self.index_tasks()

  def index_tasks(self):
    index = 1
    for task in self.body:
      task.tag.tag_index = str(index)
      task.tag.tag_edit.set_caption(task.tag.build_caption())
      index += 1

  def move_focus(self, trans):
    focus_task = self.list_box.focus
    if focus_task:
      sub_focus = focus_task.pile.focus
      if sub_focus == focus_task.expan:
        try:
          sub_focus.expan_pile.focus_position += trans
        except IndexError:
          try:
            focus_task.pile.focus_position += trans
          except IndexError:
            try:
              self.list_box.focus_position += trans
            except IndexError:
              pass
      else:
        try:
          focus_task.pile.focus_position += trans
        except IndexError:
          try:
            self.list_box.focus_position += trans
          except IndexError:
            pass
