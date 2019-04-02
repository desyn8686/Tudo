from urwid import WidgetWrap, Edit, Text, Filler, LineBox, Pile


class GroupFilter(WidgetWrap):
  
  def __init__(self):
    self.edit = Edit(caption='Group= ', edit_text='', align='center')
    self.line_box = LineBox(self.edit)
    super().__init__(Filler(self.line_box))
