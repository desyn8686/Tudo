# title_bar.py
from urwid import Edit, AttrSpec, AttrMap, WidgetWrap

class TitleBar(WidgetWrap):
 
  def __init__(self, title):
    self.edit = Edit(edit_text=title, align='center')
    self.map = AttrMap(self.edit, AttrSpec('yellow', 'black'))
    super().__init__(self.map)
