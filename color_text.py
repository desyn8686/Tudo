import urwid

colors = []
for i in range(255):
 color = 'h' + str(i)
 colors.append(urwid.Edit((urwid.AttrSpec(color, ''), color)))

urwid.MainLoop(urwid.ListBox(urwid.SimpleFocusListWalker(colors))).run()
