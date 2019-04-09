from urwid import WidgetWrap, Edit, Text, Filler, LineBox, Pile

class ConfirmDelete(WidgetWrap):
  def __init__(self):
    self.target = None
    self.header = Text('', align='center', wrap='clip')
    self.line = Text('', align='center')
    self.keys = Edit('(y/n)', align='center')
    self.pile = Pile([self.header, self.line, self.keys])
    self.line_box = LineBox(self.pile)
    super().__init__(Filler(self.line_box))

  def keypress(self, size, key):
    if key == 'enter' or key == 'esc' or key == 'n':
      return 'clear'
    elif key == 'y':
      self.target.delete_focus()
      return 'clear'
    else:
      return

  def set_edit_text(self, line_type, text):
    self.header.set_text('Delete ' + line_type + ':')    
    if len(text) > 28:
      text = text[0:25] + '...'
    self.line.set_text(text)

