# overlay_pane.py
from tudo.reminder import Reminder
from tudo.subject_selector import SubjectSelector
import urwid

class OverlayPane(urwid.WidgetWrap):
  
  signals = ['save']
  def __init__(self, tlist_manager):
    self.manager = tlist_manager
    self.holder = urwid.WidgetPlaceholder(self.manager)
    super().__init__(self.holder)

  def set_overlay(self, overlay):
    if not overlay:
      self.holder.original_widget = self.manager
    elif overlay == 'save':
      save_overlay = _SaveOverlay(self.manager)
      urwid.connect_signal(save_overlay, 'close', self.save_callback)
      self.holder.original_widget = save_overlay
    elif overlay == 'reminder':
      reminder_overlay = _ReminderOverlay(self.manager)
      self.holder.original_widget = reminder_overlay

  def save_callback(self, obj, arg):
      self.set_overlay(None)
      self._emit('save', arg)

  def keypress(self, size, key):
    if not self.manager.is_editing():
      if key == 'Q':
        self.set_overlay('save')
      elif key == 'R':
        self.set_overlay('reminder')
      else: return super().keypress(size, key)
    else: return super().keypress(size, key)

      
class _SaveOverlay(urwid.WidgetWrap):
 
  signals = ['close']
  def __init__(self, manager):
    prompt = "Closing Tudo\n" +\
             "------------\n" +\
             "Would you like to save\n" +\
             "before quitting?\n" +\
             "------------\n" +\
             "(y/n/esc)"
    text = urwid.Text(prompt, align='center')
    text._selectable = True
    fill = urwid.Filler(text)
    line_box = urwid.LineBox(fill)
    overlay = urwid.Overlay(line_box, manager, 'center', 28, 'middle', 8) 
    super().__init__(overlay)

  def keypress(self, size, key):
    if key == 'y':
      self._emit('close', 'yes')
    elif key == 'n':
      self._emit('close', 'no')
    elif key == 'esc':
      self._emit('close', 'abort')

class _ReminderOverlay(urwid.WidgetWrap):

  def __init__(self, manager):
    self.reminder = Reminder() 
    self.manager = manager
    self.header = urwid.Text('Set a reminder for:\n' +\
                             '------------', 'center')
    self.holder = urwid.WidgetPlaceholder(urwid.Filler(urwid.Text('')))
    self.frame = urwid.Frame(self.holder, header=self.header)
    self.box_adapter = urwid.BoxAdapter(self.frame, self.get_height())
    line_box = urwid.LineBox(self.box_adapter)
    overlay = urwid.Overlay(line_box, manager, 'center', 30, 'middle', 'pack') 
    super().__init__(overlay)

    self.select_subject()

  def signal_handler(self, obj, args):
    if args[0] == 'subject':
      self.set_subject(args[1], args[2])

  def select_subject(self):
    subject = SubjectSelector(self.manager)
    urwid.connect_signal(subject, 'select', self.signal_handler)
    self.holder.original_widget = subject
    self.box_adapter.height = self.get_height()
  
  def set_subject(self, callback_string, obj_id):
    self.reminder.reminder_type = callback_string
    self.reminder.reminder_id = obj_id

  def get_height(self):
    height = 0
    height += self.header.pack()[1]
    try:
      height += self.holder.original_widget.get_height()
    except AttributeError:
      pass
    return height
