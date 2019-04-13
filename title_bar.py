# title_bar.py
from change_prompt import ChangePrompt
from urwid import Edit, AttrSpec, AttrMap, WidgetWrap
import urwid

class TitleBar(urwid.WidgetWrap):
 
  def __init__(self, title):
    self.title = _Title(title)
    urwid.connect_signal(self.title, 'rebuild', self.build_stack)
    self.holder = urwid.WidgetPlaceholder(None)
    self.build_stack()
    super().__init__(self.holder)

  def get_title(self):
    return self.title.text.text

  def edit(self):
    self.title.start_edit()

  def delete(self):
    self.test = urwid.Text('meowmeow')
    self.padding = urwid.Padding(self.test, 'center', 'pack')
    self.holder.original_widget = self.padding

  def build_stack(self, obj=None):
    pack = self.title.pack()[0]
    length = pack if pack else 1
    self.padding = urwid.Padding(self.title, 'center', length)
    self.map = AttrMap(self.padding, AttrSpec('yellow', 'black'))
    self.holder.original_widget = self.map

class _Title(urwid.PopUpLauncher):

  signals = ['rebuild']
  def __init__(self, title):
    self.text = urwid.Text(title, align='center')
    super().__init__(self.text)

  def start_edit(self):
    self.original_text = self.text.text
    self.open_pop_up()

  def update_change(self, obj):
    self.text.set_text(obj.edit.edit_text)
    self._emit('rebuild')

  def save_change(self, obj):
    self.text.set_text(str.strip(obj.edit.edit_text))
    self.original_text = self.text.text    
    self.close_pop_up()
    self._emit('rebuild')

  def abort_change(self, obj):
    self.text.set_text(self.original_text)
    self.close_pop_up()
    self._emit('rebuild')

  def create_pop_up(self):
    prompt = ChangePrompt(self.text.text)
    urwid.connect_signal(prompt, 'save', self.save_change)
    urwid.connect_signal(prompt, 'abort', self.abort_change)
    urwid.connect_signal(prompt, 'update', self.update_change)
    return prompt

  def get_pop_up_parameters(self):
    return {'left': -1, 'top': 0, 'overlay_width': len(self.text.text)+2, 'overlay_height': 1} 
