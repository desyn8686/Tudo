from tlist_manager import TListManager
import urwid 

tlm = TListManager()
loop = urwid.MainLoop(tlm)
try:
  loop.run()
except KeyboardInterrupt:
  tlm.save_and_quit()  
  print('Goodbye!')
