import tlist_io
import prompt
import sys
from tlist_browser import TListBrowser
from tlist_manager import TListManager
from tlist_filter import TListFilter
from group_filter import GroupFilter
from confirm_delete import ConfirmDelete
from urwid import MainLoop, Pile, LineBox, Edit, Overlay, Filler, WidgetWrap
from urwid import connect_signal, WidgetPlaceholder

class Handler():
  
  def __init__(self):
    self.grab_next = False

  def unhandled_keys(self, key):
    extra = None
    if len(key) == 2:
      tup = key
      key = tup[0]
      extra = tup[1]

    if key == 'F': holder.original_widget = foverlay
    elif key == 'G': holder.original_widget = goverlay
    elif key == 'N': 
      tlm.tlists.set_filter('')
      tlm.tlists.set_group('')
      tlm.new()
    elif key == 'clear': 
      holder.original_widget = tlm
    elif key == 'delete task':
      cd.target = extra
      cd.set_edit_text('Task', extra.list_box.focus.tag.tag_edit.edit_text)
      holder.original_widget = cdoverlay
    elif key == 'delete expan':
      cd.target = extra
      cd.set_edit_text('Expan', extra.expan.expan_pile.focus.edit.edit_text)
      holder.original_widget = cdoverlay
    elif key == 'delete list':
      cd.target = extra
      cd.set_edit_text('Todo List', extra.columns.focus.name)
      holder.original_widget = cdoverlay
    elif key == 'quit':
      loop.stop()
      print('Goodbye!')
      sys.exit()

     

def filter_tlists(_, new_filter):
  tlm.tlists.set_filter(new_filter)
  tlm.fill()

def filter_group(_, new_group):
  tlm.tlists.set_group(new_group)
  tlm.fill()

tlm = TListManager()
tlf = TListFilter()
tlg = GroupFilter()
nl = prompt.NewList()
cd = ConfirmDelete()

handler = Handler()

holder = WidgetPlaceholder(tlm)
connect_signal(tlf.edit, 'change', filter_tlists)
connect_signal(tlg.edit, 'change', filter_group)
foverlay = Overlay(tlf, tlm, 'center', 32, 'middle', 3)
goverlay = Overlay(tlg, tlm, 'center', 32, 'middle', 3)
nloverlay = Overlay(nl, tlm, 'center', 32, 'middle', 3)
cdoverlay = Overlay(cd, tlm, 'center', 32, 'middle', 5)
loop = MainLoop(holder, unhandled_input=handler.unhandled_keys)
try:
  loop.run()
except KeyboardInterrupt:
  tlm.save_and_quit()  
  print('Goodbye!')
