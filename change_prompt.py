import urwid

class ChangePrompt(urwid.WidgetWrap):
  
  signals = ['abort', 'save', 'update']
  def __init__(self, text, caption=None):
    self.edit = urwid.Edit(edit_text=text, align='center')
    if caption: self.edit.set_caption(caption)
    self.map = urwid.AttrMap(self.edit, urwid.AttrSpec('h231', 'h160'))
    self.fill = urwid.Filler(self.map)
    super().__init__(self.fill)

  def keypress(self, size, key):
    if key == 'enter':
      self._emit('save')
    elif key == 'esc':
      self.response = 'cancel'
      self._emit('abort')
    elif len(self.edit.edit_text) >= 25:
      if key == 'backspace':
        super().keypress(size, key)
        self._emit('update')
      else:
        pass
    else:
      super().keypress(size, key)
      self._emit('update')
