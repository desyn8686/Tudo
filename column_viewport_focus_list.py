# column_viewport_focus_list.py

from urwid.raw_display import Screen
import time

class ColumnViewportFocusList():

  def __init__(self, max_visible=4, min_columns=36):
    self.screen = Screen()
    self.max_visible = max_visible
    self.min_cols = min_columns
    self.contents = []
    self.index = 0
    self.focus = 0
    self.visible = 0
    self.filter = ''
    self.group = ''

  def get_viewport(self):
    self._find_visible()
    tlists = self._filter_contents()
      
    slice_len = len(tlists[self.index:len(tlists)]) 
    max_index = (len(tlists) - self.visible)
    if max_index < 0: max_index = 0

    if self.visible > slice_len < len(tlists):
      diff = self.visible - slice_len
      self.focus += diff
      self.index -= diff
    if self.focus > (self.visible - 1): 
      diff = self.focus - (self.visible - 1)
      self.focus -= diff
      self.index += diff
    elif self.focus < 0:
      self.index += self.focus
      self.focus = 0

    if self.index > max_index:
      self.index = max_index
    elif self.index < 0:
      self.index = 0

    viewport_list = []
    for i in range(self.visible):
      try:
        viewport_list.append(tlists[self.index + i])
      except IndexError:
        pass
    return viewport_list
     
  def _filter_contents(self):
    group_contents = []
    for tlist in self.contents:
      if self.group in tlist.group:
        group_contents.append(tlist)
    filtered_contents = []
    for tlist in group_contents:
      if self.filter in tlist.name:
        filtered_contents.append(tlist) 
    return filtered_contents 

  def _find_visible(self):
    screen_dims = self.screen.get_cols_rows() 
    cols = screen_dims[0]
    self.visible = int(cols/self.min_cols)
    if self.visible > self.max_visible: self.visible = self.max_visible 
    if self.visible > len(self._filter_contents()): self.visible = len(self._filter_contents())

  def trans_view(self, translation):
    new_index = self.index + translation
    max_index = (len(self.contents) - self.visible)
    if new_index < 0:
      new_index = 0
    elif new_index > max_index: 
      new_index = max_index
    self.index = new_index

  def append(self, item):
    self.contents.append(item)

  def insert(self, item):
    self.contents.insert((self.index + self.focus), item)

  def set_filter(self, new_filter):
    self.index = 0
    self.filter = new_filter

  def set_group(self, new_group):
    self.index = 0
    self.group = new_group

if __name__ == "__main__":
  vList = ColumnViewportFocusList()
  vList.insert("meow")
  vList.insert("cat")
  vList.focus = 1
  vList.insert("poo")
  while True:
    print(vList.get_viewport())
    time.sleep(.5)
