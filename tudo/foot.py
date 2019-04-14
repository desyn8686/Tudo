from urwid import WidgetWrap, Text, Edit, AttrMap, AttrSpec, Columns

class Foot(WidgetWrap):
  
  def __init__(self):
    
    text = Text('meow', align='center')
    text2 = Text('meow2', align='center')
    text3 = Text('meow3', align='center')
    text4 = Text('meow4', align='center')

    texts = [text, text2, text3, text4]

    self.columns = Columns(texts)
    super().__init__(self.columns)
