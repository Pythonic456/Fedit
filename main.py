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
widget_maintextedit = tktools.TextEditor(frame_maintextedit)


menubar = tktools.MenuBar(frame_menubar)


def open_file():
    global ftypes, widget_maintextedit
    f_name = tkfd.askopenfilename(filetypes=ftypes, initialdir=os.path.expanduser('~'))
    f_text = open(f_name, 'r').read()
    widget_maintextedit.set_text(text=f_text)

def save_file():
    global ftypes, widget_maintextedit
    f_name = tkfd.asksaveasfilename(filetypes=ftypes, initialdir=os.path.expanduser('~'))
    if f_name is None:
        return
    text = widget_maintextedit.get_text(0.0)
    f_obj = open(f_name, 'w')
    f_obj.write(text)
    f_obj.close()




menubar.add_button('open', open_file, 'Open')
menubar.add_button('save', save_file, 'Save')

menubar.grid_button('open', row=0, column=0)
menubar.grid_button('save', row=0, column=1)


widget_maintextedit.pack(expand=1, fill='both')

frame_menubar.pack(side='top', expand=1, fill='both')
frame_maintextedit.pack(expand=1, fill='both')

root.mainloop()
print('Exiting')