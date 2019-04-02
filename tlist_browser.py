# tlist_browser.py
from urwid import Frame, Columns, Filler, WidgetWrap, ListBox, LineBox, SimpleFocusListWalker, Button, AttrMap, AttrSpec, Text, Edit

class TListBrowser(WidgetWrap):
  
  def __init__(self, tlists, groups):
    self.tlist_body = SimpleFocusListWalker([])
    self.group_body = SimpleFocusListWalker([])
    self.tabs = []
    self.focus_tab = None
    
    for tlist_dict in tlists:
      self.tlist_body.append(_ListItem(tlist_dict))
    for group in [groups]:
      self.group_body.append(Edit(group))

    self.group_list_box = ListBox(self.group_body)
    self.group_line_box = LineBox(self.group_list_box)
    self.tabs.append(self.group_line_box)
      
    self.tlist_list_box = ListBox(self.tlist_body)
    self.tlist_line_box = LineBox(self.tlist_list_box)
    self.tabs.append(self.tlist_line_box)
    self.focus_tab = self.tlist_line_box

    self.list_tabs = _ListTabs()
    self.list_tabs.set_tab(1)
    self.frame = Frame(self.tabs[self.list_tabs.tab_index], header=self.list_tabs)
    super().__init__(self.frame)

  def keypress(self, size, key):
    if key == 'h':
      self.set_tab(0)
    elif key == 'l':
      self.set_tab(1)
    else:
      super().keypress(size, key)

  def set_tab(self, tab_index):
    self.list_tabs.set_tab(tab_index)
    self.change_tab(tab_index)

  def change_tab(self, tab_index):
    self.frame.contents['body'] = (self.tabs[tab_index], None)

class _ListItem(WidgetWrap):
  
  def __init__(self, tlist_dict):
    self.index = tlist_dict['index']
    self.name = tlist_dict['name']
    super().__init__(AttrMap(Button(self.name), AttrSpec('', ''), AttrSpec(', bold', '')))

class _ListTabs(WidgetWrap):

  def __init__(self):
    self.tab_index = 1 
    self.names = ['GROUPS', 'LISTS']

    self.attr_spec = AttrSpec('', '')
    self.focus_spec = AttrSpec('h14, bold', 'light gray')

    self.tabs = []
    for name in self.names:
      self.tabs.append(Text((self.attr_spec, self.format_name(name)), 'center')) 

    self.columns = Columns(self.tabs)
    super().__init__(self.columns)

  def format_name(self, name):
    return '< ' + name + ' >'

  def set_tab(self, tab_index):
    for i in range(2):
      if i == tab_index:
        self.tab_index = tab_index
        self.tabs[tab_index].base_widget.set_text((self.focus_spec, self.format_name(self.names[tab_index])))
        self.focus_tab = self.tabs[tab_index].base_widget
      else:
        self.tabs[i].base_widget.set_text((self.attr_spec, self.format_name(self.names[i])))
