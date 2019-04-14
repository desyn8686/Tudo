# task_expan.py

from tudo.conf_prompt import ConfPrompt
from urwid import WidgetWrap, Edit, AttrSpec, AttrMap, Filler, SimpleFocusListWalker, ListBox
from urwid import MainLoop, BoxAdapter, Pile
import urwid


class TaskExpan(WidgetWrap):

  signals = ['empty']
  def __init__(self, expan_lines):  

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
      strike = False
      if op_char == 'x': strike = True
      line = line.lstrip(op_char)
      expan = _Expan(line, strike)
      urwid.connect_signal(expan, 'delete', self.delete)
      widget_list.append(expan)
    return widget_list
    
  def length(self):
    return len(self.expan_list)

  def get_lines(self):
    raw_lines = []
    for line in self.expan_list:
      if line.strikethrough:
        raw_lines.append('x' + line.edit.get_edit_text())
      else:
        raw_lines.append('o' + line.edit.get_edit_text())
    return raw_lines

  def move_cursor(self, translation):
    line = self.expan_pile.focus  
    line.edit.edit_pos += translation

  def toggle_strike(self):
    line = self.expan_pile.focus
    line.toggle_strike()

  def prompt_delete(self):
    self.expan_pile.focus.open_pop_up()

  def delete(self, obj):
    for expan_tuple in self.expan_pile.contents:
      if obj in expan_tuple:
        self.expan_list.remove(obj)
        self.expan_pile.contents.remove(expan_tuple)
    if not self.expan_list:
      self._emit('empty')
  
  def new(self):
    new_expan = _Expan('new expan')
    urwid.connect_signal(new_expan, 'delete', self.delete)
    self.expan_list.append(new_expan)
    self.expan_pile.contents.append((new_expan, ('weight', 1)))
    self.expan_pile.focus_position = len(self.expan_list)-1

class _Expan(urwid.PopUpLauncher):
  
  signals = ['delete']
  def __init__(self, edit_text, strike=False):
 
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

    self.edit = Edit(caption, edit_text, wrap='clip')
    self.map = AttrMap(self.edit, attr_map=attr, focus_map=attr_focus)
    self.fill = Filler(self.map)

    super().__init__(self.map)

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

  def create_pop_up(self):
    prompt = ConfPrompt('line')
    urwid.connect_signal(prompt, 'close', self.confirm_delete)
    return prompt

  def confirm_delete(self, obj):
    response = obj.response
    if response == 'yes':
      self.close_pop_up() 
      self._emit('delete')
    else:
      self.close_pop_up()

  def get_pop_up_parameters(self):
    width = len(self.edit.text)-5 if len(self.edit.text)-5 > 21 else 21 
    return {'left': 5, 'top': 1, 'overlay_width': width, 'overlay_height': 1} 
