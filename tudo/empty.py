import urwid

class Empty(urwid.WidgetPlaceholder):
  
  def __init__(self):
    self.text = urwid.Text(
      "No lists found\n'N' to create a new list", 'center')
    self.text._selectable = True
    self.fill = urwid.Filler(self.text, valign='middle')
    super().__init__(self.fill)
