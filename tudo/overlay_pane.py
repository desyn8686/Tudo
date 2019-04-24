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
    self.header_text = 'Set a reminder for:\n'
    self.header = urwid.Text('Set a reminder for:\n' +\
                             '------------', 'center')
    self.holder = urwid.WidgetPlaceholder(urwid.Filler(urwid.Text('')))
    self.frame = urwid.Frame(self.holder, header=self.header)
    self.box_adapter = urwid.BoxAdapter(self.frame, self.get_height())
    line_box = urwid.LineBox(self.box_adapter)
    overlay = urwid.Overlay(line_box, manager, 'center', 30, 'middle', 'pack') 
    super().__init__(overlay)

    self.start_reminder()

  def signal_handler(self, obj, args):
    if args[0] == 'subject':
      self.set_subject(args[1], args[2], args[3])
    if args[0] == 'frequency':
      self.set_frequency(args[1]) 
    if args[0] == 'catagory':
      self.set_catagory(args[1])

  def start_reminder(self):
    subject = SubjectSelector(self.manager)
    urwid.connect_signal(subject, 'select', self.signal_handler)
    self.holder.original_widget = subject
    self.box_adapter.height = self.get_height()
  
  def set_subject(self, callback_string, obj_id, subject):
    self.reminder.reminder_type = callback_string
    self.reminder.reminder_id = obj_id
    self.header_text = self.header_text + subject + '\n'
    self.header.set_text(self.header_text + '------------')
    self.box_adapter.height = self.get_height()

    frequency = FrequencySelector()
    urwid.connect_signal(frequency, 'select', self.signal_handler)

    self.holder.original_widget = frequency
    self.box_adapter.height = self.get_height()

  def set_frequency(self, frequency):
    self.header_text = self.header_text + frequency
    self.header.set_text(self.header_text + '\n------------')
    if frequency == 'every':
      self.reminder.repeat = True
    elif frequency == 'once':
      catagory = CatagorySelector()  
      urwid.connect_signal(catagory, 'select', self.signal_handler)
      self.holder.original_widget = catagory 
      self.box_adapter.height = self.get_height()

  def set_catagory(self, catagory):
    self.header_text = self.header_text + ' ' + catagory 
    self.header.set_text(self.header_text + '\n------------')
    if catagory == 'in':
      pass
    elif catagory == 'at':
      pass
    elif catagory == 'on':
      pass

  def get_height(self):
    height = 0
    height += self.header.pack((30,))[1]
    try:
      height += self.holder.original_widget.get_height()
    except AttributeError:
      pass
    return height

class FrequencySelector(urwid.WidgetWrap):
    
  signals=['select']
  def __init__(self):
    self.once = 'once...'
    self.once = urwid.Text(self.once, 'center')
    self.once._selectable = True
    self.once = urwid.AttrMap(self.once,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.every = 'every...'
    self.every = urwid.Text(self.every, 'center')
    self.every._selectable = True
    self.every = urwid.AttrMap(self.every,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.columns = urwid.Columns([self.every, self.once])
    super().__init__(urwid.Filler(self.columns))

  def keypress(self, size, key):
    if key == 'h':
      try:
        self.columns.focus_position -= 1
      except IndexError:
        pass
    elif key == 'l':
      try:
        self.columns.focus_position += 1
      except IndexError:
        pass
    elif key == 'enter' or key == ' ':
      self._emit('select', ['frequency', self.columns.focus.base_widget.text.rstrip('...').lower()])

  def get_height(self):
    return 1

class CatagorySelector(urwid.WidgetWrap):

  signals=['select']
  def __init__(self):
    self.in_delta = 'in...'
    self.in_delta = urwid.Text(self.in_delta, 'center')
    self.in_delta._selectable = True
    self.in_delta= urwid.AttrMap(self.in_delta,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.at_time= 'at...'
    self.at_time= urwid.Text(self.at_time, 'center')
    self.at_time._selectable = True
    self.at_time= urwid.AttrMap(self.at_time,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.on_date = 'on...'
    self.on_date = urwid.Text(self.on_date, 'center')
    self.on_date._selectable = True
    self.on_date = urwid.AttrMap(self.on_date,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.columns = urwid.Columns([self.in_delta, self.at_time, self.on_date])
    super().__init__(urwid.Filler(self.columns))
    
  def keypress(self, size, key):
    if key == 'h':
      try:
        self.columns.focus_position -= 1
      except IndexError:
        pass
    elif key == 'l':
      try:
        self.columns.focus_position += 1
      except IndexError:
        pass
    elif key == 'enter' or key == ' ':
      self._emit('select', ['catagory', self.columns.focus.base_widget.text.rstrip('...').lower()])

  def get_height(self):
    return 1
