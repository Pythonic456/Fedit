import tktools, os
from tktools import tk, tkfd

version = '0.0.0.1'
ftypes = [
    ('All files', '*'),
    ('Python code files', '*.py'), 
    ('Perl code files', '*.pl;*.pm'),  # semicolon trick
    ('Java code files', '*.java'), 
    ('C++ code files', '*.cpp;*.h'),   # semicolon trick
    ('Text files', '*.txt'),  
]
initial_dir = os.path.expanduser('~')

print('Starting Fedit '+version)

root = tktools.Window('Fedit ('+str(version)+')').window_raw()

frame_maintextedit = tk.Frame(root)
frame_menubar = tk.Frame(root)
widget_maintextedit = tktools.TextEditor(frame_maintextedit)


menubar = tktools.MenuBar(frame_menubar)


def verify_f_name(f_name):
    if f_name in [None, ()]:
        return True
    return False

def open_file():
    global ftypes, widget_maintextedit, initial_dir
    f_name = tkfd.askopenfilename(filetypes=ftypes, initialdir=initial_dir)
    if verify_f_name(f_name):
        return
    print(f_name)
    initial_dir = f_name.split('/')
    initial_dir.pop(-1)
    initial_dir = '/'.join(initial_dir)
    f_text = open(f_name, 'r').read()
    widget_maintextedit.set_text(text=f_text)

def save_file():
    global ftypes, widget_maintextedit, initial_dir
    f_name = tkfd.asksaveasfilename(filetypes=ftypes, initialdir=initial_dir)
    if not verify_f_name(f_name):
        return
    initial_dir = f_name.split('/')
    initial_dir.pop(-1)
    initial_dir = '/'.join(initial_dir)
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