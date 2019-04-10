import tlist_io
from column_viewport_focus_list import ColumnViewportFocusList
from tlist import TList
from urwid import MainLoop, WidgetWrap, WidgetPlaceholder, Overlay, Text, Filler, LineBox, ListBox, SimpleFocusListWalker, Columns
from urwid import AttrMap, AttrSpec

class TListManager(WidgetWrap):

  def __init__(self):
    self.tlists = ColumnViewportFocusList()

    loaded_lists = tlist_io.load_list_data()
    for data in loaded_lists:
      tlist = TList(data)
      self.tlists.append(tlist)

    self.columns = Columns([], min_width = 32)
    super().__init__(self.columns)

  def render(self, size, focus=False):
    self.pack()
    return super().render(size, focus)

  def new(self):
    self.tlists.insert(TList()) 
    self.pack()

  def get_lists(self):
    tlist_dicts = []
    for tlist in self.tlists.contents:
      tlist_dicts.append({'index': self.tlists.contents.index(tlist), 'name': tlist.name})
    return tlist_dicts

  def get_groups(self):
    return('meow')

  def pack(self):
    viewport_list = self.tlists.get_viewport()
    if len(self.tlists.contents) > 0:
      self.columns.contents.clear()
      options = ('weight', 1, False)
      for tlist in viewport_list:
        if tlist == None:
          column = ((Filler(Text('empty', align='center'))), options)
        else:
          column = (tlist, options)
        self.columns.contents.append(column)
      try:
        self.columns.focus_position = self.tlists.focus
      except IndexError:
        pass
    else:
      self.columns.contents.clear()

  def move_focus(self, translation):
    self.tlists.focus += translation
    self.pack()

  def keypress(self, size, key):
    if self.columns.focus.is_editing:
      return super().keypress(size, key)
    else:
      if key == 'L':
        self.move_focus(1)
      elif key == 'H':
        self.move_focus(-1)
      elif key == 'D':
        return 'delete list', self
      elif key == 'Q':
        self.save_and_quit()
        return 'quit'
      else: return super().keypress(size, key)

  def delete_focus(self):
    focus = self.columns.focus
    tlist_io.delete_list(focus.id)
    self.tlists.contents.remove(focus)
    self.pack()

  def save_and_quit(self):
    for tlist in self.tlists.contents:
      tlist_io.save_list(tlist.export())
    

if __name__ == '__main__':
  manager = TListManager()
  manager.tlists.focus = 0
  loop = MainLoop(manager)
  loop.run()
