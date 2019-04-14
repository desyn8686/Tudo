# tlist_holder.py

from tudo.conf_prompt import ConfPrompt
import urwid


class TListHolder(urwid.WidgetPlaceholder):
  
  signals = ['delete']
  def __init__(self, tlist):
    self.tlist = tlist
    super().__init__(self.tlist)

    self.deleting = False

  def prompt_delete(self):
    self.deleting = True
    prompt = ConfPrompt('list')
    urwid.connect_signal(prompt, 'close', self.confirm_delete)
    overlay = urwid.Overlay(
        top_w=urwid.LineBox(prompt), 
        bottom_w=self.tlist, 
        align='center',
        width=21,
        valign='middle',
        height=3)
    self.original_widget = overlay

  def confirm_delete(self, obj):
    if obj.response == 'yes':
      self._emit('delete')
    elif obj.response == 'no':
      self.deleting = False
      self.original_widget = self.tlist
