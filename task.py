# task.py
from task_tag import TaskTag
from task_expan import TaskExpan
from urwid import WidgetWrap, Pile 

class Task(WidgetWrap):
  
  def __init__(self, tag_index=99, task_data=None):

    self.task_data = task_data
    if not self.task_data:
      self.task_data = {}
      self.task_data['tag'] = 'oNew task' 
      self.task_data['expan'] = []

    self.show_expan = False

    # Build widget stack
    self.tag = TaskTag(tag_index, self.task_data['tag'])
    self.expan = TaskExpan(self.task_data['expan'])
    self.pile = Pile([self.tag])
    super().__init__(self.pile)

  def toggle_expan(self):
    if self.expan.length() > 0:
      if self.show_expan:
        self.show_expan = False
      else:
        self.show_expan = True 
      self.redraw_expan()

  def toggle_strike(self):
    self.pile.focus.toggle_strike()
      
  def move_cursor(self, translation):
    self.pile.focus.move_cursor(translation)

  def delete_focus(self):
    self.expan.delete_focus()
    if self.expan.length() == 0:
      self.show_expan = False
    self.redraw_expan()

  def redraw_expan(self):
    for widget_tuple in self.pile.contents:
      if self.expan in widget_tuple:
        self.pile.contents.remove(widget_tuple)
    if self.show_expan:
      self.pile.contents.append((self.expan, ('flow', None)))
