## Import modules
import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import messagebox as tkmb
import os, sys


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


# Detect broken Tk 8.6.9 which fails to handle high unicode characters (>BMP 0xffff)
# -> boolean
def is_high_unicode_ok(rootwin, verb=0):
    ttest = tk.Text(rootwin)
    u = chr(0x1F600)
    try:
        ttest.insert(tk.END, u)
        u2 = ttest.get('0.0', tk.END)[:-1]
    except:
        if verb:
            print('is_high_unicode_ok: Exception: %s' % (sys.exc_info()[1],))
        return False
    finally:
        ttest.destroy()
    if verb:
        print('is_high_unicode_ok: Expect %r, Got %r, OK %s' % (u, u2, u == u2))
    return u == u2


# Backwards compat monkey-patch for Python 3.7 or less
if sys.version_info[:2] < (3, 8):
    # Insert high unicode (>BMP) into Text widget
    def text_insert_high(self, index, chars, *args):
        print('text_insert_high() called')
        if not chars:
            return
        if ord(max(chars)) <= 0xffff:
            return self.text_insert_original(index, chars, *args)
        # TODO: better escaping of 'chars' (e.g. escape backslashes, check TCL escaping rules)
        return self.tk.eval('%s insert %s "%s"' % (self._w, index, chars.replace('"', '\\"')))
    tk.Text.text_insert_original = tk.Text.insert
    tk.Text.insert = text_insert_high
    
    # Get high unicode (>BMP) from Text widget, and decode any surrogate-pairs
    def text_get_high(self, index1, index2=None):
        chars = self.text_get_original(index1, index2)
        chars = chars.encode('utf-16', 'surrogatepass').decode('utf-16')
        return chars
    tk.Text.text_get_original = tk.Text.get
    tk.Text.get = text_get_high


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
        self.clear_text(0.0, 'end')
        self.widget.insert(0.0, text)
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
        self.__updatetitle__()
    def saveas_file(self, *args, **kwargs):
        ## Asks for a file to save the contents of the text widget
        ## in and saves it there
        #args and kwargs to this function are thrown away
        f_name = tkfd.asksaveasfilename(filetypes=self.ftypes, initialdir=self.initial_dir)
        if not verify_f_name(f_name):
            return 0
        self.__savefiledata__(f_name, self.get_text(0.0, 'end'))
        return 1
        self.__updatetitle__()
    def new_file(self, *args, **kwargs):
        ## Clears the text widget
        dscn = tkmb.askyesnocancel('Save file?', 'Do you want to save the file already open?')
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

class LabelBar:
    def __init__(self, parent):
        ## Init
        self.parent = parent
        self.labels = {}
    def add_label(self, label_name, text):
        ## Add a label
        label = tk.Label(self.parent, text=text)
        self.labels[label_name] = {'text': text, 'raw': label}
    def pack_label(self, label_name, *args, **kwargs):
        ## Pack a label
        self.labels[label_name]['raw'].pack(args, kwargs)
    def grid_label(self, label_name, *args, **kwargs):
        ## Grid a label
        self.labels[label_name]['raw'].grid(kwargs)
    def raw_label(self, label_name):
        ## Returns the raw Tk label widget
        return self.labels[label_name]['raw']
    def config_label(self, label_name, *args, **kwargs):
        self.labels[label_name]['raw'].config(kwargs)

        
if __name__=='__main__':
    print('Run main.py instead of this! Starting main.py anyway...')
    import main
