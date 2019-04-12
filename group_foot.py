from change_prompt import ChangePrompt
from urwid import WidgetWrap, Edit, AttrMap, AttrSpec
import urwid

class GroupFoot(WidgetWrap):
  
  def __init__(self, group):
    self.group = _Group(group)
    urwid.connect_signal(self.group, 'rebuild', self.build_stack)
    self.holder = urwid.WidgetPlaceholder(None)
    self.build_stack()
    super().__init__(self.holder)

  def edit(self):
    self.group.start_edit()

  def build_stack(self, obj=None):
    pack = self.group.pack()[0]
    length = pack if pack else 1
    self.padding = urwid.Padding(self.group, 'center', length)
    self.map = AttrMap(self.padding, AttrSpec('', 'black'))
    self.holder.original_widget = self.map

class _Group(urwid.PopUpLauncher):

  signals = ['rebuild']
  def __init__(self, group):
    self.edit = urwid.Edit(caption='Group: ', edit_text=group, align='center')
    super().__init__(self.edit)

  def start_edit(self):
    self.original_text = self.edit.edit_text
    self.open_pop_up()

  def create_pop_up(self):
    prompt = ChangePrompt(self.edit.edit_text, caption=self.edit.caption)
    urwid.connect_signal(prompt, 'close', self.confirm_change)
    return prompt

  def confirm_change(self, obj):
    response = obj.response
    if response == 'change':
      self.close_pop_up() 
      self.edit.set_edit_text(obj.edit.edit_text)
      self.open_pop_up()
    elif response == 'confirm':
      self.original_text = self.edit.edit_text
      self.close_pop_up()
    elif response == 'cancel':
      self.edit.set_edit_text(self.original_text)
      self.close_pop_up()
    self._emit('rebuild')

  def get_pop_up_parameters(self):
    return {'left': -1, 'top': 0, 'overlay_width': len(self.edit.text)+2, 'overlay_height': 1} 
