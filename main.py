import tktools, os
from tktools import tk, tkfd

version = '0.0.0.1'
ftypes = [
    ('Python code files', '*.py'), 
    ('Perl code files', '*.pl;*.pm'),  # semicolon trick
    ('Java code files', '*.java'), 
    ('C++ code files', '*.cpp;*.h'),   # semicolon trick
    ('Text files', '*.txt'), 
    ('All files', '*'), 
]

print('Starting Fedit '+version)

root = tktools.Window('Fedit ('+str(version)+')').window_raw()

frame_maintextedit = tk.Frame(root)
frame_menubar = tk.Frame(root)


menubar = tktools.MenuBar(frame_menubar)


def open_file():
    global ftypes
    f_name = tkfd.askopenfilename(filetypes=ftypes, initialdir=os.path.expanduser('~'))
    print(f_name)

menubar.add_button('open', open_file, 'Open')

menubar.grid_button('open', row=0, column=0)

widget_maintextedit = tktools.TextEditor(frame_maintextedit).widget_raw()


widget_maintextedit.pack(expand=1, fill='both')

frame_menubar.pack(side='top', expand=1, fill='both')
frame_maintextedit.pack(expand=1, fill='both')

root.mainloop()
print('Exiting')