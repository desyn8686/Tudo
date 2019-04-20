from tudo.tlist_manager import TListManager
from tudo.overlay_pane import OverlayPane
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

  PID = os.getpid()
  background = False
  save_on_quit = None 
  
  def __init__(self, overlay_pane):
    self.overlay = overlay_pane
    signal.signal(signal.SIGTSTP, self.SIGTSTP)
    signal.signal(signal.SIGINT, self.SIGINT)
  
  def SIGTSTP(self, signum, frame):
    signal.signal(signal.SIGTSTP, signal.SIG_DFL)
    self.background = True
    raise urwid.ExitMainLoop

  def SIGINT(self, signum, frame):
    self.overlay.set_overlay('save')
    loop.draw_screen()

  def save(self, obj, arg):
    if arg == 'abort':
      pass
    else:
      self.save_on_quit = arg
      raise urwid.ExitMainLoop

def quit(obj):
  pane.set_overlay('save')

manager = TListManager(tlist_io.load_list_data())
pane = OverlayPane(manager)
sig_handler = SignalHandler(pane)

urwid.connect_signal(manager, 'quit', quit)
urwid.connect_signal(pane, 'save', sig_handler.save)

event = urwid.SelectEventLoop()
loop = urwid.MainLoop(pane, event_loop=event, pop_ups=True, handle_mouse=True)

while True:
  with loop.start():
    try:
      event.run()
    except KeyboardInterrupt:
      pane.set_overlay('save')
  if sig_handler.background:
    os.kill(sig_handler.PID, signal.SIGTSTP)
    sig_handler.background = False
    signal.signal(signal.SIGTSTP, sig_handler.SIGTSTP)
  elif sig_handler.save_on_quit:
    if sig_handler.save_on_quit == 'yes':
      tlist_io.save_all(manager.pull_list_data())
    elif sig_handler.save_on_quit == 'no':
      print('Closing without saving')
    break
print('Goodbye!')
