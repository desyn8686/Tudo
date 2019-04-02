# task_expan.py

from urwid import WidgetWrap, Edit, AttrSpec, AttrMap, Filler, SimpleFocusListWalker, ListBox
from urwid import MainLoop, BoxAdapter, Pile


class TaskExpan(WidgetWrap):

  def __init__(self, expan_lines):  

    self.lines = []


    # Build widget stack
    self.expan_list = self.build_lines(expan_lines)
    self.expan_pile = Pile([])
    for line in self.expan_list:
      self.expan_pile.contents.append((line, ('weight', 1)))
    super().__init__(self.expan_pile)
    
  def build_lines(self, lines):
    widget_list = []
    for line in lines:
      op_char = line[0]
      strike = None
      if op_char == 'o': strike = False
      elif op_char == 'x': strike = True
      line = line.lstrip(op_char)
      expan = _Expan(line, strike)
      widget_list.append(expan)
    return widget_list
    
  def length(self):
    return len(self.expan_list)

  def get_lines(self):
    raw_lines = []
    for line in self.lines:
      raw_lines.append(line.get_edit_text())
    return raw_lines

  def move_cursor(self, translation):
    line = self.expan_pile.focus.base_widget  
    line.edit_pos += translation

  def toggle_strike(self):
    line = self.expan_pile.focus
    line.toggle_strike()


class _Expan(WidgetWrap):
  
  def __init__(self, edit_text, strike):
 
    self.strikethrough = strike
    self.leading_space = '   '
    self.leading_char = '- '
    self.leading_STRIKE = 'x '

    # Default color specs
    self.text_attr = AttrSpec('h6', '')
    self.text_STRIKE = AttrSpec('h6, strikethrough', '')
    self.focus_attr = AttrSpec('h6, bold', '')
    self.focus_STRIKE = AttrSpec('h6, bold, strikethrough', '')

    if not self.strikethrough:
      caption = self.leading_space + self.leading_char
      attr = self.text_attr
      attr_focus = self.focus_attr
    else:
      caption = self.leading_space + self.leading_STRIKE
      attr = self.text_STRIKE
      attr_focus = self.focus_STRIKE

    self.edit = Edit(caption, edit_text)
    self.map = AttrMap(self.edit, attr_map=attr, focus_map=attr_focus)
    self.fill = Filler(self.map)

    super().__init__(self.fill)

  def toggle_strike(self):
    if self.strikethrough:
      self.strikethrough = False
      attr = self.text_attr
      attr_focus = self.focus_attr
      self.map.set_attr_map({None: attr})
      self.map.set_focus_map({None: attr_focus})
      self.edit.set_caption(self.leading_space + self.leading_char)
    else:
      self.strikethrough = True
      caption = self.leading_space + self.leading_STRIKE
      attr = self.text_STRIKE
      attr_focus = self.focus_STRIKE
      self.map.set_attr_map({None: attr})
      self.map.set_focus_map({None: attr_focus})
      self.edit.set_caption(self.leading_space + self.leading_STRIKE)
    

if __name__ == "__main__":
  task = TaskExpan(['meow', 'cat'])
  loop = MainLoop(task)
  loop.run()
