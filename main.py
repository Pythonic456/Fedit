import tktools
from tktools import os, tk, sys
from tkinter import colorchooser, messagebox
from ast import literal_eval

version = '0.0.1.5'

print('Starting Fedit', version)
print('Home dir:', os.path.expanduser('~'))

root_title = 'Fedit ('+str(version)+')'
root = tktools.Window(root_title).window_raw()

def set_root_title(title):
    root.title(title)
    root.update()


## Config file
def load_config_file():
    global config
    print('Loading config file...', end=' ')
    with open(os.path.expanduser('~/.fedit'), 'r') as config_file_obj:
        config = {}
        for line in config_file_obj:
            tup = line.split(',', 1)
            # Use rstrip() to remove trailing newline
            config[tup[0]] = tup[1].rstrip()
    print('Done', config)

if os.path.isfile(os.path.expanduser('~/.fedit')):
    load_config_file()
else:
    print('First time running Fedit, creating config file...', end=' ')
    config_file_obj = open(os.path.expanduser('~/.fedit'), 'w')
    print(os.path.expanduser('~/.fedit'))
    import requests
    data = requests.get('https://smallbytes.pythonanywhere.com/Fedit/newuser')
    config_file_obj.write(str(data.content, encoding='ascii'))
    config_file_obj.close()
    load_config_file()
print(config)

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
themes = literal_eval(config['Themes'])

def update_theme(theme, text_theme, button_theme, button_text_theme, custom=0):
    print('Custom:', custom, 'BG:', theme, 'FG:', text_theme)
    root.config(bg=theme)
    widget_maintextedit.config(bg=theme, fg=text_theme, insertbackground=text_theme)
    frame_menubar.config(bg=theme)
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
    
    # Emoticons (Unicode block): U+1F600 to U+1F64F
    emojis = range(0x1F600, 0x1F64F + 1)
    
    win = tktools.Window('Emojis', root_win=root).window_raw()
    for row, echunk in enumerate(chunks(emojis, 10)):
        for col, ecode in enumerate(echunk):
            b = tk.Button(win, text=chr(ecode),
                command=lambda ecode=ecode: widget_maintextedit.widget.insert(tk.INSERT, chr(ecode)))
            b.grid(column=col, row=row)
menubar.add_button('emojis', emoji_window, '☺')
menubar.grid_button('emojis', row=0, column=5)


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
