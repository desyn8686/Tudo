from tudo.tlist_manager import TListManager
import tudo.tlist_io as tlist_io
import urwid 
import signal
import os

'''
This is important!
We need to catch the SIGTSTP signal
so we can exit the main loop
and then properly execute the signal
by calling it again.
'''
class SignalHandler():

  background = False
  
  def SIGTSTP(self, signum, frame):
    signal.signal(signal.SIGTSTP, signal.SIG_DFL)
    self.background = True
    raise urwid.ExitMainLoop

def save():
  list_data = manager.pull_list_data()  
  tlist_io.save_all(list_data)

sig_handler = SignalHandler()
PID = os.getpid()
signal.signal(signal.SIGTSTP, sig_handler.SIGTSTP)

manager = TListManager(tlist_io.load_list_data())
event = urwid.SelectEventLoop()
loop = urwid.MainLoop(manager, event_loop=event, pop_ups=True, handle_mouse=True)

while True:
  with loop.start():
    try:
      event.run()
    except KeyboardInterrupt:
      save()
      break
  if sig_handler.background:
    os.kill(PID, signal.SIGTSTP)
    sig_handler.background = False
    signal.signal(signal.SIGTSTP, sig_handler.SIGTSTP)

print('Goodbye!')
