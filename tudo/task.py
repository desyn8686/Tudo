# task.py
from tudo.task_tag import TaskTag
from tudo.task_expan import TaskExpan
from urwid import WidgetWrap, Pile 
import urwid

class Task(WidgetWrap):

  show_expan = False
  signals = ['delete'] 
  def __init__(self, tag_index=99, task_data=None):
    self.task_data = task_data
    if not self.task_data:
      self.task_data = {}
      self.task_data['tag'] = 'oNew task' 
      self.task_data['expan'] = []

    # Build widget stack
    self.tag = TaskTag(tag_index, self.task_data['tag'])
    urwid.connect_signal(self.tag, 'delete', self.delete)
    self.expan = TaskExpan(self.task_data['expan'])
    urwid.connect_signal(self.expan, 'empty', self.close_expan)
    self.pile = Pile([self.tag])
    super().__init__(self.pile)

  def toggle_expan(self):
    if self.expan.length() > 0:
      if self.show_expan:
        self.show_expan = False
      else:
        self.show_expan = True 
      self.redraw_expan()

  def close_expan(self, obj=None):
    self.show_expan = False
    self.redraw_expan()
    
  def open_expan(self, obj=None):
    if self.expan.length() > 0:
      self.show_expan = True 
      self.redraw_expan()

  def redraw_expan(self):
    for widget_tuple in self.pile.contents:
      if self.expan in widget_tuple:
        self.pile.contents.remove(widget_tuple)
    if self.show_expan:
      self.pile.contents.append((self.expan, ('weight', 1)))
      self.pile.focus_position = 1 

  def new(self):
    self.expan.new()
    self.show_expan = True
    self.redraw_expan()

  def prompt_delete(self):
    self.pile.focus.prompt_delete()

  def delete(self, obj):
    self._emit('delete')

  def toggle_strike(self):
    self.pile.focus.toggle_strike()
      
  def move_cursor(self, translation):
    self.pile.focus.move_cursor(translation)
