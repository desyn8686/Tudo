from tudo.tlist_manager import TListManager
import tudo.tlist_io as tlist_io
import urwid 
import signal
import os

#class SuspendProcess(Exception):
#  pass

#def suspend(signum, frame):
#  raise SuspendProcess

#signal.signal(signal.SIGTSTP, suspend)

tlm = TListManager(tlist_io.load_list_data())
loop = urwid.MainLoop(tlm, pop_ups=True, handle_mouse=True)
running = True
while running:
  try:
    loop.run()
  except KeyboardInterrupt:
    data = tlm.pull_list_data()  
    tlist_io.save_all(data)
    running = False
print('Goodbye!')