import urwid

class ConfPrompt(urwid.WidgetWrap):

  prompt_head = "^Delete "
  prompt_tail = "? (y/n)"
  
  signals = ['close']  
  def __init__(self, obj_type):
    self.response = ''
    self.text = urwid.Text(self.prompt_head + obj_type + self.prompt_tail, align='center')
    self.map = urwid.AttrMap(self.text, urwid.AttrSpec('h231', 'h160'))
    self.fill = urwid.Filler(self.map)
    super().__init__(self.fill)

  def keypress(self, size, key):
    if key == 'y':
      self.response = 'yes'
      self._emit('close')
    elif key == 'n' or key == 'esc':
      self.response = 'no'
      self._emit('close')
