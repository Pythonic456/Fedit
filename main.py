#!/usr/bin/python3
import tktools
from tktools import os, tk, sys
from tkinter import colorchooser, messagebox
from ast import literal_eval

version = '0.0.1.6'

print('Starting Fedit', version)
FNCONF = os.path.expanduser('~/.fedit')
print('Config file:', FNCONF)

root_title = 'Fedit ('+str(version)+')'
root = tktools.Window(root_title).window_raw()

def set_root_title(title):
    root.title(title)
    root.update()


## Config file
def load_config_file():
    global config
    print('Loading config file...', end=' ')
    with open(FNCONF, 'r') as config_file_obj:
        config = {}
        for line in config_file_obj:
            tup = line.split(',', 1)
            # Use rstrip() to remove trailing newline
            config[tup[0]] = tup[1].rstrip()
    print('Done', config)

if os.path.isfile(FNCONF):
    load_config_file()
else:
    print('First time running Fedit, creating config file...', end=' ')
    config_file_obj = open(FNCONF, 'w')
    print(FNCONF)
    import requests
    data = requests.get('https://smallbytes.pythonanywhere.com/Fedit/newuser')
    config_file_obj.write(str(data.content, encoding='ascii'))
    config_file_obj.close()
    load_config_file()
themes = literal_eval(config['Themes'])

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

## LabelBar
frame_labelbar = tk.Frame(root)
labelbar = tktools.LabelBar(frame_labelbar)

labelbar.add_label('chars', '0')
labelbar.grid_label('chars', row=0)
labelbar.config_label('chars', bg=themes[False]['buttons'], fg=themes[False]['buttons_text'])

def update_labelbar_chars(*args, **kwargs):
    labelbar.config_label('chars', text=str(len(widget_maintextedit.widget_raw().get(0.0, 'end'))-1))
widget_maintextedit.widget_raw().bind('<Any-KeyRelease>', update_labelbar_chars)

## Theme
theme_current = False #False=Light True=Dark

def update_theme(theme, text_theme, button_theme, button_text_theme, custom=0):
    print('Custom:', custom, 'BG:', theme, 'FG:', text_theme)
    root.config(bg=theme)
    widget_maintextedit.config(bg=theme, fg=text_theme, insertbackground=text_theme)
    frame_menubar.config(bg=theme)
    frame_labelbar.config(bg=theme)
    for button in menubar.buttons:
        menubar.buttons[button]['raw'].config(bg=button_theme, fg=button_text_theme)

def switch_theme():
    global theme_current
    theme_current = not theme_current
    messages = {True: 'Switching theme to Dark', False: 'Switching theme to Light'}
    print(messages[theme_current])
    theme = themes[theme_current]
    update_theme(theme['main'], themes[not theme_current]['main'], theme['buttons'], theme['buttons_text'])
    root.update()

def set_theme():
    bg_col = colorchooser.askcolor(title='Choose background colour')[1]
    fg_col = colorchooser.askcolor(title='Choose foreground colour')[1]
    bt_col = colorchooser.askcolor(title='Choose button background colour')[1]
    btt_col = colorchooser.askcolor(title='Choose button foreground colour')[1]
    update_theme(bg_col, fg_col, bt_col, btt_col, custom=1)

def prefs_window():
    win = tktools.Window('Preferences', root_win=root).window_raw()
    button_switch_theme = tk.Button(win, text='Switch Theme', command=switch_theme)
    button_set_theme = tk.Button(win, text='Set Theme', command=set_theme)
    button_switch_theme.pack(fill='both', expand=1)
    button_set_theme.pack(fill='both', expand=1)

menubar.add_button('prefs', prefs_window, 'Prefrences')
switch_theme()

menubar.grid_button('prefs', row=0, column=4)


def emoji_window():
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    
    emojis = [
        '\u2639', # WHITE FROWNING FACE
        '\u263a', # WHITE SMILING FACE
        '\u263b', # BLACK SMILING FACE
        '\u263c', # WHITE SUN WITH RAYS
        '\u263d', # FIRST QUARTER MOON
        '\u263e', # LAST QUARTER MOON
    ]
    
    # Emoticons (Unicode block): U+1F600 to U+1F64F
    if tktools.is_high_unicode_ok(root, verb=1):
        emojis.extend([chr(i) for i in range(0x1F600, 0x1F64F + 1)])
    
    win = tktools.Window('Emojis', root_win=root).window_raw()
    for row, echunk in enumerate(chunks(emojis, 10)):
        for col, ucode in enumerate(echunk):
            b = tk.Button(win, command=lambda ucode=ucode: widget_maintextedit.widget.insert(tk.INSERT, ucode))
            # b['text'] = ucode # Does not work in Python 3.7
            b.tk.eval('%s configure -text "%s"' % (b._w, ucode))
            b.grid(column=col, row=row)
menubar.add_button('emojis', emoji_window, '\u263a')
menubar.grid_button('emojis', row=0, column=5)


## Packing
frame_menubar.pack(side='top', expand=1, fill='both')
frame_maintextedit.pack(expand=1, fill='both')
frame_labelbar.pack(side='bottom', expand=1, fill='both')

## Complete exit
def complete_exit():
    if messagebox.askokcancel("Quit", "Do you want to quit? The open file may not be saved."):
        root.destroy()
        print('Exiting via Quit')
        sys.exit()

root.protocol("WM_DELETE_WINDOW", complete_exit)

## Start the window
root.mainloop()

## Exited
print('Exiting')
