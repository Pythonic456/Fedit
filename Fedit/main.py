import tktools
from tktools import tk

print('Starting')

version = '0.0.0.1'

root = tktools.Window('Fedit ('+str(version)+')').window_raw()

widget_maintextedit = tktools.TextEditor(root).widget_raw()
widget_maintextedit.pack()

root.mainloop()
print('Exiting')