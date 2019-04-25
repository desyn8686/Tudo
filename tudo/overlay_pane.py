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
    self.div = '\n--------------------------'
    self.header = urwid.Text('Set a reminder for:' +\
                             self.div, 'center')
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
    elif args[0] == 'frequency':
      self.set_frequency(args[1]) 
    elif args[0] == 'category':
      self.set_category(args[1])
    elif args[0] == 'in':
      self.set_in_delta(args[1], args[2])

  def start_reminder(self):
    subject = SubjectSelector(self.manager)
    urwid.connect_signal(subject, 'select', self.signal_handler)
    self.holder.original_widget = subject
    self.box_adapter.height = self.get_height()
  
  def set_subject(self, callback_string, obj_id, subject):
    self.reminder.reminder_type = callback_string
    self.reminder.reminder_id = obj_id
    self.header_text = [self.header_text, (urwid.AttrSpec('h11', ''), subject)]
    self.header.set_text([self.header_text, self.div]) 
    self.box_adapter.height = self.get_height()

    frequency = FrequencySelector()
    urwid.connect_signal(frequency, 'select', self.signal_handler)

    self.holder.original_widget = frequency
    self.box_adapter.height = self.get_height()

  def set_frequency(self, frequency):
    self.header_text = [self.header_text, ' ', (urwid.AttrSpec('h85', ''), frequency)]
    self.header.set_text([self.header_text, self.div])
    if frequency == 'every':
      self.reminder.repeat = True
    elif frequency == 'once':
      category = CatagorySelector()  
      urwid.connect_signal(category, 'select', self.signal_handler)
      self.holder.original_widget = category 
      self.box_adapter.height = self.get_height()

  def set_category(self, category):
    self.header_text = [self.header_text, ' ', category]
    self.header.set_text([self.header_text, self.div])
    if category == 'in':
      in_selector = InSelector()
      urwid.connect_signal(in_selector, 'select', self.signal_handler)
      self.holder.original_widget = in_selector
    elif category == 'at':
      pass
    elif category == 'on':
      pass
    self.box_adapter.height = self.get_height()

  def set_in_delta(self, hours, minutes):
    delta_string = ''
    days = 0

    hours = int(hours)
    minutes = int(minutes)

    hours += int(minutes/60)
    minutes = minutes%60
    days += int(hours/24)
    hours = hours%24

    if days > 0:
      self.reminder.in_days = days
      delta_string = [delta_string, str(days), ' days']
    if hours > 0:
      self.reminder.in_hours = hours 
      if days > 0: delta_string = [delta_string, ', ']
      delta_string = [delta_string, str(hours), ' hours']
    if minutes > 0:
      self.reminder.in_mins = minutes 
      if hours > 0: delta_string = [delta_string, ', and ']
      delta_string = [delta_string, str(minutes), ' minutes.']
      
    self.reminder.build()
    self.header_text = [self.header_text, ' ', (urwid.AttrSpec('h166', ''), delta_string)]
    self.header_text = [self.header_text, '\n', '(', self.reminder.dt_string, ')']
    self.header.set_text([self.header_text, self.div])

    conf_selector = ConfirmationSelector()
    urwid.connect_signal(conf_selector, 'select', self.signal_handler)
    self.holder.original_widget = conf_selector
    self.box_adapter.height = self.get_height()

  def get_height(self):
    height = 0
    height += self.header.pack((28,))[1]
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
    self.columns = urwid.Columns([self.once, self.every])
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
      self._emit('select', ['category', self.columns.focus.base_widget.text.rstrip('...').lower()])

  def get_height(self):
    return 1

class InSelector(urwid.WidgetWrap):

  signals=['select']
  def __init__(self):
    self.hours_edit = urwid.IntEdit('  Hours: ')
    self.minutes_edit = urwid.IntEdit('Minutes: ')

    self.body = urwid.SimpleListWalker([self.hours_edit, self.minutes_edit])
    self.list_box = urwid.ListBox(self.body)
    super().__init__(urwid.Filler(urwid.BoxAdapter(self.list_box, 3)))

  def get_height(self):
    return 2 

  def keypress(self, size, key):
    if key == 'k':
      try:
        self.list_box.focus_position -= 1
      except IndexError:
        pass
    elif key == 'j':
      try:
        self.list_box.focus_position += 1
      except IndexError:
        pass
    elif key == 'enter' or key == ' ':
      try:
        self.list_box.focus_position += 1
      except IndexError:
        self._emit('select', ['in', self.hours_edit.edit_text, self.minutes_edit.edit_text])
    elif key == 'h' or key == 'left':
      try:
        self.list_box.focus.edit_pos -= 1
      except IndexError:
        pass
    elif key == 'l' or key == 'right':
      try:
        self.list_box.focus.edit_pos += 1
      except IndexError:
        pass
    else: 
      focus = self.list_box.focus.base_widget
      if focus.valid_char(key) and focus.edit_text == '0':
        focus.set_edit_text('')
      num_length = len(self.list_box.focus.edit_text)
      if key == 'backspace' or key == 'delete': return super().keypress(size, key)
      else: 
        if num_length < 3: return super().keypress(size, key)


  def render(self, size, focus=False):
    for edit in self.body:
      if edit.edit_text == '':
        edit.set_edit_text('0')
    return super().render(size, focus)

class ConfirmationSelector(urwid.WidgetWrap):

  signals=['select']
  def __init__(self):
    self.confirm_prompt = urwid.Text('Set reminder?', 'center') 
    self.yes = 'yes'
    self.yes = urwid.Text(self.yes, 'center')
    self.yes._selectable = True
    self.yes= urwid.AttrMap(self.yes,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.no = 'no'
    self.no = urwid.Text(self.no, 'center')
    self.no._selectable = True
    self.no = urwid.AttrMap(self.no,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.columns = urwid.Columns([self.yes, self.no])
    self.body = urwid.SimpleListWalker([self.confirm_prompt, self.columns])
    self.list_box = urwid.ListBox(self.body)
    super().__init__(self.list_box)
    
  def get_height(self):
    return 2
    
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
      pass
