import tkinter as tk
from tkinter import ttk
from records import get_credits

class Sidebar:
    def __init__(self, window: tk.Tk, username: str, expand: bool = False):
        self.username = username
        self.window = window
        self.min_width = 0
        self.max_width = 120

        self.frame = ttk.Frame(self.window, height = self.window.winfo_height(), width = self.max_width)
        self.frame.grid(row = 0, column = 0)
        self.frame.grid_propagate(False)

        if not expand:
            self.cur_width = self.min_width
            self.expanded = False
            self.side_btn = ttk.Button(self.frame, text = "≡", width = 3, command = self.change)
        else:
            self.cur_width = self.max_width
            self.expanded = True
            self.side_btn = ttk.Button(self.frame, text = "|||", width = 3)

        self.side_btn.grid(row = 0, column = 0, pady = 10, padx = 10, sticky = "w")

        self.sidebar = ttk.Frame(self.frame, height = self.window.winfo_height(), width = self.cur_width, style = "Card.TFrame")
        self.sidebar.grid(row = 1, column = 0, sticky = "w")
        self.sidebar.grid_propagate(False)

        self.home_btn = ttk.Button(self.sidebar, text = "Home", style = "Accent.TButton", command = lambda m = 0: self.open_tab(m))
        self.green_btn = ttk.Button(self.sidebar, text = "Book a ride", style = "Accent.TButton", command = lambda m = 1: self.open_tab(m))
        self.posts_btn = ttk.Button(self.sidebar, text = "Allow lifts", style = "Accent.TButton", command = lambda m = 2: self.open_tab(m))
        self.events_btn = ttk.Button(self.sidebar, text = "Profile", style = "Accent.TButton", command = lambda m = 3: self.open_tab(m))
        self.notifs_btn = ttk.Button(self.sidebar, text = "Notifications", style = "Accent.TButton", command = lambda m = 4: self.open_tab(m))
        self.logout_btn = ttk.Button(self.sidebar, text = "Log out", style = "Accent.TButton", command = lambda m = 5: self.open_tab(m))
        self.credits_lbl = ttk.Label(self.sidebar, text = f"Credits: {get_credits(self.username)}")
        self.home_btn.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "ew")
        self.green_btn.grid(row = 1, column = 0, padx = 10, sticky = "ew")
        self.posts_btn.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "ew")
        self.events_btn.grid(row = 3, column = 0, padx = 10, sticky = "ew")
        self.notifs_btn.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = "ew")
        self.logout_btn.grid(row = 5, column = 0, padx = 10, sticky = "ew")
        self.credits_lbl.grid(row = 6, column = 0, padx = 10, pady = 10)

        self.expanded = False
    
    def change(self):
        if not self.expanded:
            rep = self.window.after(5, self.change)
            self.cur_width += 10
            self.sidebar.config(width = self.cur_width)
            if self.cur_width >= self.max_width:
                self.window.after_cancel(rep)
                self.expanded = True
                self.side_btn.config(text = "|||")
        else:
            rep = self.window.after(5, self.change)
            self.cur_width -= 10
            self.sidebar.config(width = self.cur_width)
            if self.cur_width <= self.min_width:
                self.window.after_cancel(rep)
                self.expanded = False
                self.side_btn.config(text = "≡")

    def open_tab(self, index):
        self.window.destroy()
        if index == 0:
            from home_page import Home
            Home(self.username)
        elif index == 1:
            from book_page import Book
            Book(self.username)
        elif index == 2:
            from lifts_page import Lifts
            Lifts(self.username)
        elif index == 3:
            from profile_page import Profile
            Profile(self.username)
        elif index == 4:
            from notifications_page import Notifications
            Notifications(self.username)
        elif index == 5:
            from login_page import Login
            Login()
