# task.py
from task_tag import TaskTag
from task_expan import TaskExpan
from urwid import WidgetWrap, Pile 

class Task(WidgetWrap):
  
  def __init__(self, tag_index, task_data):

    self.show_expan = False

    # Build widget stack
    self.tag = TaskTag(tag_index, task_data['tag'])
    self.expan = TaskExpan(task_data['expan'])
    self.task_pile = Pile([(1, self.tag)])
    super().__init__(self.task_pile)

  def toggle_expan(self):
    if self.show_expan:
      for widget_tuple in self.task_pile.contents:
        if self.expan in widget_tuple:
          self.task_pile.contents.remove(widget_tuple)
      self.show_expan = False
    else:
      self.task_pile.contents.append((self.expan, ('given', self.expan.length())))
      self.show_expan = True 

  def toggle_strike(self):
    self.task_pile.focus.toggle_strike()
      
  def move_cursor(self, translation):
    self.task_pile.focus.move_cursor(translation)
