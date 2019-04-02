from urwid import WidgetWrap, Edit, Text, Filler, LineBox, Pile


class TListFilter(WidgetWrap):
  
  def __init__(self):
    self.edit = Edit(caption='Filter= ', edit_text='', align='center')
    self.line_box = LineBox(self.edit)
    super().__init__(Filler(self.line_box))
