import tktools
from tktools import tk

print('Starting')

version = '0.0.0.1'

root = tktools.Window('Fedit ('+str(version)+')').window_raw()

frame_maintextedit = tk.Frame(root)

widget_maintextedit = tktools.TextEditor(frame_maintextedit).widget_raw()
widget_maintextedit.pack(expand=1, fill='both')

frame_maintextedit.pack(expand=1, fill='both')

root.mainloop()
print('Exiting')