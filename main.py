import tktools
from tktools import os, tk
from tkinter import colorchooser

version = '0.0.1.5'

print('Starting Fedit', version)
print('Home dir:', os.path.expanduser('~'))

root_title = 'Fedit ('+str(version)+')'
root = tktools.Window(root_title).window_raw()

def set_root_title(title):
    root.title(title)
    root.update()

## Main text editor
frame_maintextedit = tk.Frame(root)
widget_maintextedit = tktools.TextEditor(frame_maintextedit, root_title, set_root_title)

## MenuBar
frame_menubar = tk.Frame(root)
menubar = tktools.MenuBar(frame_menubar)

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
    win = tktools.Window('Preferences', root_win=root).window_raw()
    button_switch_theme = tk.Button(win, text='Switch Theme', command=switch_theme)
    button_set_theme = tk.Button(win, text='Set Theme', command=set_theme)
    button_switch_theme.pack(fill='both', expand=1)
    button_set_theme.pack(fill='both', expand=1)

menubar.add_button('prefs', prefs_window, 'Prefrences')
update_theme(theme_light, theme_dark)

menubar.grid_button('prefs', row=0, column=4)


## Packing
frame_menubar.pack(side='top', expand=1, fill='both')
frame_maintextedit.pack(expand=1, fill='both')

## Start the window
root.mainloop()

## Exited
print('Exiting')