# subject_selector.py
import urwid

class SubjectSelector(urwid.WidgetWrap):

  signals = ['select']
  def __init__(self, manager):
    self.manager = manager
    div = urwid.Text('----------------------------')
    #div = urwid.Text('------')
    task_info = self.manager.get_focus('task')
    list_info = self.manager.get_focus('list')
    group_info = self.manager.get_focus('group')

    task = SubjectText("Task-: " +\
                          task_info[0],
                          task_info[1],
                          'task')
    task = urwid.AttrMap(task,
                         attr_map=urwid.AttrSpec('', ''),
                         focus_map=urwid.AttrSpec('h10', ''))
    tlist = SubjectText('List-: ' +\
                           list_info[0], 
                           list_info[1], 
                           'list')
    tlist = urwid.AttrMap(tlist, 
                          attr_map=urwid.AttrSpec('', ''),
                          focus_map=urwid.AttrSpec('h10', ''))
    group = SubjectText('Group: ' +\
                           group_info[0],
                           group_info[1],
                           'group')
    group = urwid.AttrMap(group,
                          attr_map=urwid.AttrSpec('', ''),
                          focus_map=urwid.AttrSpec('h10', ''))

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
      self._emit('select', 
                 ['subject',
                 self.list_box.focus.base_widget.callback_string,
                 self.list_box.focus.base_widget.obj_id,
                 self.list_box.focus.base_widget.text])

  def get_height(self):
    height = 0
    for line in self.body:
      height += line.pack((30,))[1] 
    return height

  def height(self):
    return self.box_adapter.height

  def render(self, size, focus=False):
    return super().render(size, focus)
      
class SubjectText(urwid.Text):
  
  _selectable = True

  def __init__(self, text, obj_id, callback):
    self.callback_string = callback
    self.obj_id = obj_id
    super().__init__(text)

  def keypress(self, size, key):
    pass
