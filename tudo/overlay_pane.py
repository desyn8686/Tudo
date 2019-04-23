# overlay_pane.py
from tudo.reminder import Reminder
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

  def select_subject(self):
    subject = SubjectSelector(self.manager)
    urwid.connect_signal(subject, 'select', self.signal_handler)
    self.holder.original_widget = subject
    self.box_adapter.height = self.get_height()
  
  def set_subject(self, subject, contents):
    print(subject)

  def signal_handler(self, obj, args):
    if args[0] == 'subject':
      self.set_subject(args[1], args[2])

  def frequency(self):
    every = urwid.Text('every', align='center')

  def get_height(self):
    height = 0
    height += self.header.pack()[1]
    try:
      height += self.holder.original_widget.get_height()
    except AttributeError:
      pass
    return height


class SelectableText(urwid.Text):
  
  _selectable = True

  def __init__(self, text, return_text):
    self.return_text = return_text
    super().__init__(text)

  def keypress(self, size, key):
    pass


class SubjectSelector(urwid.WidgetWrap):

  signals = ['select']
  def __init__(self, manager):
    self.manager = manager
    div = urwid.Text('----------------------------')
    #div = urwid.Text('------')
    task = SelectableText("Task-: " +\
                      self.manager.get_focus('task').get_text(),
                      self.manager.get_focus('task'))#, 'center')
    task = urwid.AttrMap(task, attr_map=urwid.AttrSpec('', ''), focus_map=urwid.AttrSpec('h10', ''))
    tlist = SelectableText('List-: ' +\
                       self.manager.get_focus('list').name,
                       self.manager.get_focus('list'))#, 'center')
    tlist = urwid.AttrMap(tlist, attr_map=urwid.AttrSpec('', ''), focus_map=urwid.AttrSpec('h10', ''))
    group = SelectableText('Group: ' +\
                       self.manager.get_focus('group')[0],
                       self.manager.get_focus('group')[1])#, 'center')
    group = urwid.AttrMap(group, attr_map=urwid.AttrSpec('', ''), focus_map=urwid.AttrSpec('h10', ''))
    self.body = urwid.SimpleListWalker([task, div, tlist, div, group])
    self.list_box = urwid.ListBox(self.body)
    self.box_adapter = urwid.BoxAdapter(self.list_box, self.get_height())
    super().__init__(urwid.Filler(self.box_adapter))

  def keypress(self, size, key):
    if key == 'k':
      try:
        self.list_box.focus_position -= 2
      except IndexError:
        pass
    elif key == 'j':
      try:
        self.list_box.focus_position += 2
      except IndexError:
        pass
    elif key == ' ' or key == 'enter':
      self._emit('select', ['subject', self.list_box.focus.base_widget.return_text, self.list_box.focus.base_widget.text])

  def get_height(self):
    height = 0
    for line in self.body:
      height += line.pack((30,))[1] 
    return height

  def height(self):
    return self.box_adapter.height

  def render(self, size, focus=False):
    return super().render(size, focus)
      
