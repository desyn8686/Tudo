# title_bar.py
from change_prompt import ChangePrompt
from urwid import Edit, AttrSpec, AttrMap, WidgetWrap
import urwid

class TitleBar(urwid.WidgetWrap):
 
  def __init__(self, title):
    self.title = _Title(title)
    urwid.connect_signal(self.title, 'rebuild', self.rebuild_stack)
    self.padding = urwid.Padding(self.title, 'center', self.title.pack()[0])
    self.map = AttrMap(self.padding, AttrSpec('yellow', 'black'))
    self.holder = urwid.WidgetPlaceholder(self.map)
    super().__init__(self.holder)

  def change(self):
    self.title.change()

  def rebuild_stack(self, obj):
    pack = self.title.pack()[0]
    length = pack if pack else 1
    self.padding = urwid.Padding(self.title, 'center', length)
    self.map = AttrMap(self.padding, AttrSpec('yellow', 'black'))
    self.holder.original_widget = self.map

class _Title(urwid.PopUpLauncher):

  signals = ['rebuild']
  def __init__(self, title):
    self.text = urwid.Text(title, align='center')
    self.holder = urwid.WidgetPlaceholder(self.text)
    super().__init__(self.holder)

  def change(self):
    self.original_text = self.text.text
    self.open_pop_up()

  def create_pop_up(self):
    prompt = ChangePrompt(self.text.text)
    urwid.connect_signal(prompt, 'close', self.confirm_change)
    return prompt

  def confirm_change(self, obj):
    response = obj.response
    if response == 'change':
      self.close_pop_up() 
      self.text.set_text(obj.edit.edit_text)
      self.open_pop_up()
    elif response == 'confirm':
      self.original_text = self.text.text
      self.close_pop_up()
    elif response == 'cancel':
      self.text.set_text(self.original_text)
      self.close_pop_up()
    self._emit('rebuild')

  def get_pop_up_parameters(self):
    return {'left': -1, 'top': 0, 'overlay_width': len(self.text.text)+2, 'overlay_height': 1} 
