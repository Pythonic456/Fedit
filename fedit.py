#!/usr/bin/env python3
## Import modules
import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import messagebox as tkmb
import os
from tkinter import colorchooser


## Classes
def verify_f_name(f_name):
    if f_name in [None, (), '']:
        return False
    return True

root_window = False
root_window_obj = None
class Window:
    def __init__(self, title, root_win=None):
        global root_window, root_window_obj
        self.title = title
        if root_window == False:
            self.win = tk.Tk()
            root_window_obj = self.win
        else:
            self.win = tk.Toplevel()
        self.win.title(self.title)
        
    def window_raw(self):
        return self.win


class TextEditor:
    def __init__(self, parent, root_title, set_root_title):
        ## Init
        self.parent = parent
        self.widget = tk.Text(self.parent)
        self.ftypes = [
            ('All files', '*'),
            ('Python code files', '*.py'), 
            ('Perl code files', '*.pl;*.pm'),  # semicolon trick
            ('Java code files', '*.java'), 
            ('C++ code files', '*.cpp;*.h'),   # semicolon trick
            ('Text files', '*.txt'),  
        ]
        self.initial_dir = os.path.expanduser('~')
        self.curr_file = None
        self.set_root_title = set_root_title
        self.root_title = root_title
    def __savefiledata__(self, f_name, data):
        print('Saving', f_name)
        self.initial_dir = os.path.dirname(f_name)
        f_obj = open(f_name, 'w')
        f_obj.write(data)
        f_obj.close()
        self.curr_file = f_name
    def __updatetitle__(self, f_name=None):
        if f_name == None:
            f_name = self.curr_file
        if f_name == None:
            self.set_root_title(self.root_title)
        else:
            self.set_root_title(self.root_title+' - '+f_name)
    def widget_raw(self):
        ## Return the raw Tk text widget
        return self.widget
    def pack(self, *args, **kwargs):
        ## Pack the text widget
        self.widget.pack(kwargs)
    def grid(self, *args, **kwargs):
        ## Grid the text widget
        self.widget.grid(kwargs)
    def clear_text(self, *args, **kwargs):
        ## Clear text from text widget
        self.widget.delete(*args, **kwargs)
    def set_text(self, text, *args, **kwargs):
        ## Clears and sets the text
        self.clear_text(0.0)
        self.widget.insert(0.0, text, args, kwargs)
    def get_text(self, *args, **kwargs):
        ## Gets the text from the text widget
        text = self.widget.get(*args, **kwargs)
        return text
    def open_file(self, *args, **kwargs):
        ## Asks for a file to open and shows it in text widget
        #args and kwargs to this function are thrown away
        f_name = tkfd.askopenfilename(filetypes=self.ftypes, initialdir=self.initial_dir)
        if not verify_f_name(f_name):
            return
        print('Opening', f_name)
        self.initial_dir = os.path.dirname(f_name)
        f_text = open(f_name, 'r').read()
        self.set_text(text=f_text)
        self.curr_file = f_name
        self.__updatetitle__()
    def save_file(self, *args, **kwargs):
        if verify_f_name(self.curr_file):
            #Save file as currently open file
            self.__savefiledata__(self.curr_file, self.get_text(0.0))
        else:
            #No file currently open
            self.saveas_file()
    def saveas_file(self, *args, **kwargs):
        ## Asks for a file to save the contents of the text widget
        ## in and saves it there
        #args and kwargs to this function are thrown away
        f_name = tkfd.asksaveasfilename(filetypes=self.ftypes, initialdir=self.initial_dir)
        if not verify_f_name(f_name):
            return 0
        self.__savefiledata__(f_name, self.get_text(0.0))
        return 1
    def new_file(self, *args, **kwargs):
        ## Clears the text widget
        dscn = tkmb.askyesnocancel('Save file?', 'Do you want to save the file already open?') #dscn = Desicion
        if dscn == True: #User said yes
            if self.save_file() == 0:
                self.new_file()
                return
        elif dscn == None: #User cancelled
            return
        #User has saved/pressed no
        self.clear_text(0.0, 'end')
        self.curr_file = None
        self.__updatetitle__()
    def config(self, **kwargs):
        #print(kwargs)
        self.widget_raw().config(kwargs)


class MenuBar:
    def __init__(self, parent):
        ## Init
        self.parent = parent
        self.buttons = {}
    def add_button(self, button_name, command, text):
        ## Add a button
        button = tk.Button(self.parent, text=text, command=command)
        self.buttons[button_name] = {'cmd': command, 'text': text, 'raw': button}
    def pack_button(self, button_name, *args, **kwargs):
        ## Pack a button
        self.buttons[button_name]['raw'].pack(args, kwargs)
    def grid_button(self, button_name, *args, **kwargs):
        ## Grid a button
        self.buttons[button_name]['raw'].grid(kwargs)
    def raw_button(self, button_name):
        ## Returns the raw Tk button widget
        return self.buttons[button_name]['raw']
    def config_button(self, button_name, *args, **kwargs):
        self.buttons[button_name]['raw'].config(args, kwargs)



version = '0.0.1.5'

print('Starting Fedit', version)
print('Home dir:', os.path.expanduser('~'))

root_title = 'Fedit ('+str(version)+')'
root = Window(root_title).window_raw()

def set_root_title(title):
    root.title(title)
    root.update()

## Main text editor
frame_maintextedit = tk.Frame(root)
widget_maintextedit = TextEditor(frame_maintextedit, root_title, set_root_title)

## MenuBar
frame_menubar = tk.Frame(root)
menubar = MenuBar(frame_menubar)

menubar.add_button('open', widget_maintextedit.open_file, 'Open')
menubar.add_button('save', widget_maintextedit.save_file, 'Save')
menubar.add_button('saveas', widget_maintextedit.saveas_file, 'Save As')
menubar.add_button('new', widget_maintextedit.new_file, 'New')

menubar.grid_button('open', row=0, column=0)
menubar.grid_button('save', row=0, column=1)
menubar.grid_button('saveas', row=0, column=2)
menubar.grid_button('new', row=0, column=3)

## Main text editor
widget_maintextedit.pack(expand=1, fill='both')

## Theme
theme_current = False #False=Light True=Dark
theme_light = '#f5f5f5'
theme_dark = '#000000'
def update_theme(theme, text_theme, custom=0):
    print('Custom:', custom, 'BG:', theme, 'FG:', text_theme)
    root.config(bg=theme)
    widget_maintextedit.config(bg=theme, fg=text_theme, insertbackground=text_theme)
    frame_menubar.config(bg=theme)
    for button in menubar.buttons:
        menubar.buttons[button]['raw'].config(bg=theme, fg=text_theme)

def switch_theme():
    global theme_current
    theme_current = not theme_current
    messages = {True: 'Switching theme to Dark', False: 'Switching theme to Light'}
    print(messages[theme_current])
    if theme_current == True:
        update_theme(theme_dark, theme_light)
    else:
        update_theme(theme_light, theme_dark)
    root.update()

def set_theme():
    bg_col = colorchooser.askcolor(title='Choose background colour')[1]
    fg_col = colorchooser.askcolor(title='Choose foreground colour')[1]
    update_theme(bg_col, fg_col, custom=1)

def prefs_window():
    win = Window('Preferences', root_win=root).window_raw()
    button_switch_theme = tk.Button(win, text='Switch Theme', command=switch_theme)
    button_set_theme = tk.Button(win, text='Set Theme', command=set_theme)
    button_switch_theme.pack(fill='both', expand=1)
    button_set_theme.pack(fill='both', expand=1)

menubar.add_button('prefs', prefs_window, 'Prefrences')
update_theme(theme_light, theme_dark)

menubar.grid_button('prefs', row=0, column=4)

## Experimental
changing_theme = [0, 0, 0]
def changing_theme_func():
    global changing_theme
    for i, item in enumerate(changing_theme):
        item += 1
        if item > 255:
            item = 0
            #changing_theme[i] = item
        else:
            changing_theme[i] = item
            break
    if changing_theme == [255,255,255]:
        changing_theme = [0,0,0]
    update_theme('#%02x%02x%02x' % tuple(changing_theme), '#000000')
    root.after(10, changing_theme_func)
#changing_theme_func()



## Packing
frame_menubar.pack(side='top', expand=1, fill='both')
frame_maintextedit.pack(expand=1, fill='both')

## Start the window
root.mainloop()

## Exited
print('Exiting')