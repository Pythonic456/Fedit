import tkinter as tk

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
