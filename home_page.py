import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar

class Home:
    def __init__(self, username: str):
        self.window = tk.Tk()
        self.window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.window.tk.call("set_theme", "dark")
        self.window.geometry("500x500")
        self.window.update()

        self.sidebar = Sidebar(self.window, username)

        self.window.mainloop()