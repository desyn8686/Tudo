from urwid import WidgetWrap, Edit, AttrMap, AttrSpec

class GroupFoot(WidgetWrap):
  
  def __init__(self, group):
    self.edit = Edit(caption='Group: ', edit_text=group, align='center')
    self.map = AttrMap(self.edit, AttrSpec('white', 'black'))
    super().__init__(self.map)
