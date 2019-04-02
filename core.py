import tlist_io
from tlist_browser import TListBrowser
from tlist_manager import TListManager
from tlist_filter import TListFilter
from group_filter import GroupFilter
from urwid import MainLoop, Pile, LineBox, Edit, Overlay, Filler, WidgetWrap
from urwid import connect_signal, WidgetPlaceholder

def unhandled_keys(key):
  if key == 'F': holder.original_widget = foverlay
  elif key == 'G': holder.original_widget = goverlay
  elif key == 'esc': holder.original_widget = tlm

def filter_tlists(_, new_filter):
  tlm.tlists.set_filter(new_filter)
  tlm.fill()

def filter_group(_, new_group):
  tlm.tlists.set_group(new_group)
  tlm.fill()

tlm = TListManager()
tlf = TListFilter()
tlg = GroupFilter()

holder = WidgetPlaceholder(tlm)
connect_signal(tlf.edit, 'change', filter_tlists)
connect_signal(tlg.edit, 'change', filter_group)
foverlay = Overlay(tlf, tlm, 'center', 32, 'middle', 3)
goverlay = Overlay(tlg, tlm, 'center', 32, 'middle', 3)
loop = MainLoop(holder, unhandled_input=unhandled_keys)
loop.run()
