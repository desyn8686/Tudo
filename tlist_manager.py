from column_viewport_focus_list import ColumnViewportFocusList
from tlist import TList
from urwid import MainLoop, WidgetWrap, WidgetPlaceholder, Overlay, Text, Filler, LineBox, ListBox, SimpleFocusListWalker, Columns
from urwid import AttrMap, AttrSpec

class TListManager(WidgetWrap):

  def __init__(self, tlist_data):
    self.tlists = ColumnViewportFocusList()
    self.build_tlists(tlist_data)
    self.columns = Columns([], min_width = 32)
    super().__init__(self.columns)

  def build_tlists(self, tlist_data):
    for data in tlist_data:
      tlist = TList(data)
      self.tlists.append(tlist)

  def build_new(self):
    self.tlists.insert(TList()) 
    self.pack()

  def pack(self):
    viewport = self.tlists.get_viewport()
    if len(self.tlists.contents) > 0:
      self.columns.contents.clear()
      options = ('weight', 1, False)
      for tlist in viewport:
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

  def delete_focus(self):
    focus = self.columns.focus
    tlist_io.delete_list(focus.id)
    self.tlists.contents.remove(focus)
    self.pack()

  def pull_list_data(self):
    tlist_data = []
    for tlist in self.tlists.contents:
      tlist_data.append(tlist.export())
    return tlist_data

  def keypress(self, size, key):
    if self.columns.focus.is_editing:
      return super().keypress(size, key)
    else:
      if key == 'L':
        self.move_focus(1)
      elif key == 'H':
        self.move_focus(-1)
      else: return super().keypress(size, key)

  def render(self, size, focus=False):
    self.pack()
    return super().render(size, focus)
