import urwid

class ChangePrompt(urwid.WidgetWrap):
  
  signals = ['close']
  def __init__(self, text):
    self.reponse = ''
    self.edit = urwid.Edit(edit_text=text, align='center')
    self.map = urwid.AttrMap(self.edit, urwid.AttrSpec('h231', 'h160'))
    self.fill = urwid.Filler(self.map)
    super().__init__(self.fill)

  def keypress(self, size, key):
    if key == 'enter':
      self.response = 'confirm'
      self._emit('close')
    elif key == 'esc':
      self.response = 'cancel'
      self._emit('close')
    elif len(self.edit.edit_text) > 20:
      pass
    else:
      super().keypress(size, key)
      self.response = 'change'
      self._emit('close')
