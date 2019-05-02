from tudo.column_viewport_focus_list import ColumnViewportFocusList
from tudo.tlist import TList
from tudo.empty import Empty
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

  def pull_list_data(self):
    tlist_data = []
    for holder in self.tlists.contents:
      tlist_data.append(holder.tlist.export())
    return tlist_data, self.tlists.deleted

  def keypress(self, size, key):
    holder = self.columns.focus
    if holder.deleting:
      return super().keypress(size, key)
    elif self.empty:
      if key == 'N':      
        self.build_new()
      return
    elif holder.tlist.is_editing:
      return super().keypress(size, key)
    else:
      if key == 'meta D':
        holder.prompt_delete()
      elif key == 'L':
        self.move_focus(1)
      elif key == 'H':
        self.move_focus(-1)
      elif key == 'N':
        self.build_new()
      else: return super().keypress(size, key)

  def is_editing(self):
    holder = self.columns.focus
    return holder.tlist.is_editing

  def get_focus(self, obj_type):
    tlist = self.columns.focus.tlist
    if obj_type == "task":
      return tlist.get_focus().tag.get_text(), [tlist.id, tlist.get_focus().id]
    elif obj_type == 'list':
      return tlist.name, [tlist.id]
    elif obj_type == 'group':
      group = tlist.group
      group_list = []
      for _tlist in self.tlists.contents:
        if _tlist.original_widget.group == group:
          group_list.append(tlist.base_widget.id) 
      return tlist.base_widget.group, group_list

  def render(self, size, focus=False):
    self.pack()
    return super().render(size, focus)
