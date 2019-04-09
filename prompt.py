from urwid import WidgetWrap, Edit, Text, Filler, LineBox, Pile

class NewList(WidgetWrap):

  def __init__(self):
    self.text = Text('Create a new list? (y/n)', align='center')
    self.line_box = LineBox(self.text)
    super().__init__(Filler(self.line_box))

  def keypress(self, size, key):
    if key == 'y':
      print(key)
    elif key == 'n':
      print(key)


class Filter(WidgetWrap):
  
  def __init__(self):
    self.edit = Edit(caption='Filter= ', edit_text='', align='center')
    self.line_box = LineBox(self.edit)
    super().__init__(Filler(self.line_box))
    
class Group(WidgetWrap):
  
  def __init__(self):
    self.edit = Edit(caption='Group= ', edit_text='', align='center')
    self.line_box = LineBox(self.edit)
    super().__init__(Filler(self.line_box))
