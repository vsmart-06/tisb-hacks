import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
from records import *

class Book:
    def __init__(self, username: str):
        self.username = username

        self.window = tk.Tk()
        self.window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.window.tk.call("set_theme", "dark")
        self.window.geometry("500x500")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1, padx = 20, pady = 10)

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()