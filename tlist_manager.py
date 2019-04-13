from column_viewport_focus_list import ColumnViewportFocusList
from tlist import TList
from empty import Empty
from urwid import MainLoop, WidgetPlaceholder, Overlay, Text, Filler, LineBox, ListBox, SimpleFocusListWalker, Columns
from urwid import AttrMap, AttrSpec
import urwid


class TListManager(urwid.WidgetWrap):

  def __init__(self, tlist_data):
    urwid.register_signal(ColumnViewportFocusList, ColumnViewportFocusList.signals)
    self.tlists = ColumnViewportFocusList()
    urwid.connect_signal(self.tlists, 'pack', self.pack)
    self.build_tlists(tlist_data)
    self.columns = Columns([], min_width = 32)
    super().__init__(self.columns)

  def build_tlists(self, tlist_data):
    for data in tlist_data:
      print('Building tlist: ' + data['id'])
      tlist = TList(data)
      self.tlists.append(tlist)

  def build_new(self):
    self.tlists.insert(TList()) 
    self.pack()

  def pack(self):
    viewport = self.tlists.get_viewport()
    self.columns.contents.clear()
    options = ('weight', 1, False)
    if len(self.tlists.contents) > 0:
      self.empty = False
      for holder in viewport:
        column = (holder, options)
        self.columns.contents.append(column)
      try:
        self.columns.focus_position = self.tlists.focus
      except IndexError:
        pass
    else:
      self.empty = True
      self.columns.contents.append((Empty(), options))

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
    holder = self.columns.focus
    if not self.empty and holder.tlist.is_editing:
      return super().keypress(size, key)
    elif not self.empty:
      if key == 'D':
        holder.prompt_delete()
      elif key == 'L':
        self.move_focus(1)
      elif key == 'H':
        self.move_focus(-1)
      elif key == 'N':
        self.build_new()
      else: return super().keypress(size, key)
    else:
      if key == 'N':      
        self.build_new()

  def render(self, size, focus=False):
    self.pack()
    return super().render(size, focus)
