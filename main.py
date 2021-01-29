import tktools
from tktools import *

version = '0.0.0.2'


initial_dir = os.path.expanduser('~')

print('Starting Fedit '+version)

root = tktools.Window('Fedit ('+str(version)+')').window_raw()

frame_maintextedit = tk.Frame(root)
frame_menubar = tk.Frame(root)
widget_maintextedit = tktools.TextEditor(frame_maintextedit)


menubar = tktools.MenuBar(frame_menubar)


menubar.add_button('open', widget_maintextedit.open_file, 'Open')
menubar.add_button('save', widget_maintextedit.save_file, 'Save')

menubar.grid_button('open', row=0, column=0)
menubar.grid_button('save', row=0, column=1)


widget_maintextedit.pack(expand=1, fill='both')

frame_menubar.pack(side='top', expand=1, fill='both')
frame_maintextedit.pack(expand=1, fill='both')

root.mainloop()
print('Exiting')