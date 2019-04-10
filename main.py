from tlist_manager import TListManager
import tlist_io
import urwid 

tlm = TListManager(tlist_io.load_list_data())
loop = urwid.MainLoop(tlm)
try:
  loop.run()
except KeyboardInterrupt:
  tlm.save_and_quit()  
  print('Goodbye!')
