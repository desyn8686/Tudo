# overlay_pane.py
from tudo.reminder import Reminder
from tudo.subject_selector import SubjectSelector
from calendar import monthrange, IllegalMonthError
from datetime import datetime
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

  def start_reminder(self):
    subject = SubjectSelector(self.manager)
    urwid.connect_signal(subject, 'select', self.signal_handler)
    self.holder.original_widget = subject
    self.box_adapter.height = self.get_height()

  def signal_handler(self, obj, args):
    if args[0] == 'subject':
      self.set_subject(args[1], args[2], args[3])
    elif args[0] == 'frequency':
      self.set_frequency(args[1]) 
    elif args[0] == 'category':
      self.set_category(args[1])
    elif args[0] == 'in':
      self.set_in_delta(args[1], args[2])
    elif args[0] == 'every':
      self.set_every_delta(args[1])
    elif args[0] == 'starting':
      self.set_starting(args[1])

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
      every_selector = EverySelector()
      urwid.connect_signal(every_selector, 'select', self.signal_handler)
      self.holder.original_widget = every_selector
    elif frequency == 'once':
      category = CatagorySelector()  
      urwid.connect_signal(category, 'select', self.signal_handler)
      self.holder.original_widget = category 
    self.box_adapter.height = self.get_height()

  def set_category(self, category):
    self.header_text = [self.header_text, ' ', (urwid.AttrSpec('h85', ''), category)]
    self.header.set_text([self.header_text, self.div])
    if category == 'in':
      in_selector = InSelector()
      urwid.connect_signal(in_selector, 'select', self.signal_handler)
      self.holder.original_widget = in_selector
    elif category == 'at':
      pass
    elif category == 'on':
      on_selector = OnSelector()
      urwid.connect_signal(on_selector, 'select', self.signal_handler)
      self.holder.original_widget = on_selector
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
      if days > 1: delta_string = [delta_string, str(days), ' days']
      else: delta_string = [delta_string, str(days), ' day']
    if hours > 0:
      self.reminder.in_hours = hours 
      if days > 0: delta_string = [delta_string, ', ']
      if hours > 1: delta_string = [delta_string, str(hours), ' hours']
      else: delta_string = [delta_string, str(hours), ' hour']
    if minutes > 0:
      self.reminder.in_mins = minutes 
      if hours > 0: 
        if days > 0: delta_string = [delta_string, ', and ']
        else: delta_string = [delta_string, ' and ']
      if minutes > 1: delta_string = [delta_string, str(minutes), ' minutes.']
      else: delta_string = [delta_string, str(minutes), ' minutes.']
      
    self.reminder.build()
    self.header_text = [self.header_text, ' ', (urwid.AttrSpec('h166', ''), delta_string)]
    self.header_text = [self.header_text, '\n', '(', self.reminder.dt_string, ')']
    self.header.set_text([self.header_text, self.div])

    conf_selector = ConfirmationSelector()
    urwid.connect_signal(conf_selector, 'select', self.signal_handler)
    self.holder.original_widget = conf_selector
    self.box_adapter.height = self.get_height()
    
  def set_every_delta(self, hours):
    delta_string = ''
    days = 0

    hours = int(hours)
    days += int(hours/24)
    hours = hours%24

    if days > 0:
      self.reminder.in_days = days
      if days > 1: delta_string = [delta_string, str(days), ' days']
      else: delta_string = [delta_string, str(days), ' day']
    if hours > 0:
      self.reminder.in_hours = hours 
      if days > 0: delta_string = [delta_string, ', ']
      if hours > 1: delta_string = [delta_string, str(hours), ' hours']
      else: delta_string = [delta_string, str(hours), ' hour']

    self.header_text = [self.header_text, ' ', (urwid.AttrSpec('h166', ''), delta_string)]
    self.header_text = [self.header_text, ' ', (urwid.AttrSpec('h85', ''), 'starting')]
    self.header.set_text([self.header_text, self.div])

    starting_selector = StartingSelector()
    urwid.connect_signal(starting_selector, 'select', self.signal_handler)
    self.holder.original_widget = starting_selector
    self.box_adapter.height = self.get_height()

  def set_starting(self, starting):
    if starting == 'today':
      self.header_text = [self.header_text, ' ', (urwid.AttrSpec('h166', ''), 'today'), ' at']  
    elif starting == 'on':
      self.header_text = [self.header_text, ' ', 'on']  
    elif starting == 'now':
      self.reminder.build()
      self.header_text = [self.header_text, ' ', (urwid.AttrSpec('h166', ''), 'now.')]  
      self.header_text = [self.header_text, '\n', '(', self.reminder.dt_string, ')']
      conf_selector = ConfirmationSelector()
      urwid.connect_signal(conf_selector, 'select', self.signal_handler)
      self.holder.original_widget = conf_selector

    self.header.set_text([self.header_text, self.div])
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
      self._emit('select', [
          'frequency', 
          self.columns.focus.base_widget.text.rstrip('...').lower()])

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
      self._emit('select', [
          'category',
          self.columns.focus.base_widget.text.rstrip('...').lower()])

  def get_height(self):
    return 1

class InSelector(urwid.WidgetWrap):

  signals=['select']
  def __init__(self):
    self.hours_edit = urwid.IntEdit('  Hour(s): ')
    self.minutes_edit = urwid.IntEdit('Minute(s): ')

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
      
class EverySelector(urwid.WidgetWrap):

  signals=['select']
  def __init__(self):
    self.hours_edit = urwid.IntEdit('  Hour(s): ')

    super().__init__(urwid.Filler(self.hours_edit))

  def get_height(self):
    return 1 

  def keypress(self, size, key):
    if key == 'enter' or key == ' ':
      self._emit('select', ['every', self.hours_edit.edit_text])
    elif key == 'h' or key == 'left':
      try:
        self.hours_edit.edit_pos -= 1
      except IndexError:
        pass
    elif key == 'l' or key == 'right':
      try:
        self.horus_edit.edit_pos += 1
      except IndexError:
        pass
    else: 
      if self.hours_edit.valid_char(key) and self.hours_edit.edit_text == '0':
        self.hours_edit.set_edit_text('')
      if key == 'backspace' or key == 'delete': return super().keypress(size, key)
      else: 
        num_length = len(self.hours_edit.edit_text)
        if num_length < 3: return super().keypress(size, key)


  def render(self, size, focus=False):
    if self.hours_edit.edit_text == '':
      self.hours_edit.set_edit_text('0')
    return super().render(size, focus)

class StartingSelector(urwid.WidgetWrap):

  signals = ['select']
  def __init__(self):
    self.now = 'now'
    self.now = urwid.Text(self.now, 'center')
    self.now._selectable = True
    self.now = urwid.AttrMap(self.now,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.today = 'today...'
    self.today = urwid.Text(self.today, 'center')
    self.today._selectable = True
    self.today= urwid.AttrMap(self.today,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.on_date = 'on...'
    self.on_date = urwid.Text(self.on_date, 'center')
    self.on_date._selectable = True
    self.on_date = urwid.AttrMap(self.on_date,
                              attr_map=urwid.AttrSpec('', ''),
                              focus_map=urwid.AttrSpec('h10', ''))
    self.columns = urwid.Columns([self.now, self.today, self.on_date])
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
      self._emit('select', ['starting', self.columns.focus.base_widget.text.rstrip('...').lower()])

  def get_height(self):
    return 1


class OnSelector(urwid.WidgetWrap):

  signals = ['select']
  def __init__(self):
    now = datetime.now()

    spacer = urwid.Text('-')
    self.month = urwid.IntEdit(default=now.month)
    self.month = urwid.AttrMap(self.month, urwid.AttrSpec('', 'h240'))
    self.month = urwid.Padding(self.month, 'right', 2, right=1)
    
    self.day = urwid.IntEdit(default=now.day)
    self.day = urwid.AttrMap(self.day, urwid.AttrSpec('', 'h240'))
    self.day = urwid.Padding(self.day, 'center', 2, left=1, right=1)

    self.year = urwid.IntEdit(default=str(now.year)[2:4])
    self.year = urwid.AttrMap(self.year, urwid.AttrSpec('', 'h240'))
    self.year = urwid.Padding(self.year, 'left', 2, left=1)

    self.input_columns = urwid.Columns([self.month,
                                        (1, spacer),
                                        (4, self.day),
                                        (1, spacer),
                                        self.year])

    self.mm = urwid.Text('MM ', 'right')
    self.dd = urwid.Text(' DD ', 'center')
    self.yy = urwid.Text(' YY', 'left')
    self.guide_columns = urwid.Columns([self.mm, (4, self.dd), self.yy], 1)

    self.body = urwid.SimpleListWalker([self.input_columns, self.guide_columns])
    self.list_box = urwid.ListBox(self.body)
    super().__init__(urwid.Filler(urwid.BoxAdapter(self.list_box, 28)))

  def render(self, size, focus=False):
    focus = self.input_columns.focus.base_widget
    if len(focus.edit_text.lstrip('0')) == 0:
      focus.edit_text = '00'
    elif len(focus.edit_text.lstrip('0')) == 1:
      focus.edit_text = '0' + focus.edit_text.lstrip('0')

    now = datetime.now()
    year = 0
    if int(str(now.year)[2:4]) > int(self.year.base_widget.edit_text):
      year = int(str(now.year + 100)[0:2] + self.year.base_widget.edit_text) 
    else: 
      year = int(str(now.year)[0:2] + self.year.base_widget.edit_text) 

    for widget_tup in self.input_columns.contents:
      widget = widget_tup[0]
      if widget.base_widget != focus:
        if widget == self.month:
          if int(self.month.base_widget.edit_text) > 12: self.month.base_widget.edit_text = '12'
        if widget == self.day:
          try:
            max_days = monthrange(year, int(self.month.base_widget.edit_text))[1]
            if int(self.day.base_widget.edit_text) > max_days: 
              self.day.base_widget.edit_text = str(max_days)
          except IllegalMonthError:
            pass
        if widget != self.year:
          try:
            if widget.base_widget.edit_text == '00':
              widget.base_widget.edit_text = '01'
          except AttributeError:
            pass

    if focus.edit_pos != 1:
      focus.edit_pos = 1

    return super().render(size, focus)

  def keypress(self, size, key):
    focus = self.input_columns.focus.base_widget
    if key == 'l' or key == 'right':
      try:
        self.input_columns.focus_position += 2
      except IndexError:
        pass
    elif key == 'h' or key == 'left':
      try:
        self.input_columns.focus_position -= 2
      except IndexError:
        pass
    elif key == 'backspace':
      if focus.edit_pos == 1 and len(focus.edit_text) == 2:
        return super().keypress(size, 'delete')
      else: return super().keypress(size, key)
    elif key == 'delete':
      return super().keypress(size, key)
    elif len(focus.edit_text.lstrip('0')) < 2:
      focus.set_edit_text(focus.edit_text.lstrip('0'))
      return super().keypress(size, key)

  def get_height(self):
    return 2 
