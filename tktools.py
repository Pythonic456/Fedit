import tkinter as tk
from tkinter import filedialog as tkfd

root_window = False
class Window:
    def __init__(self, title):
        global root_window
        self.title = title
        if root_window == False:
            self.win = tk.Tk()
        else:
            self.win = tk.Toplevel()
        self.win.title(self.title)
        
    def window_raw(self):
        return self.win

class TextEditor:
    def __init__(self, parent):
        self.parent = parent
        self.widget = tk.Text(self.parent)
    def widget_raw(self):
        return self.widget
    def pack(self, *args, **kwargs):
        self.widget.pack(kwargs)
    def grid(self, *args, **kwargs):
        self.widget.grid(kwargs)
    def set_text(self, text, *args, **kwargs):
        self.widget.delete(0.0)
        self.widget.insert(0.0, text, args, kwargs)

class MenuBar:
    def __init__(self, parent):
        self.parent = parent
        self.buttons = {}
    def add_button(self, button_name, command, text):
        button = tk.Button(self.parent, text=text, command=command)
        self.buttons[button_name] = {'cmd': command, 'text': text, 'raw': button}
    def pack_button(self, button_name, *args, **kwargs):
        self.buttons[button_name]['raw'].pack(args, kwargs)
    def grid_button(self, button_name, *args, **kwargs):
        self.buttons[button_name]['raw'].grid(kwargs)
    def raw_button(self, button_name):
        return self.buttons[button_name]['raw']

        