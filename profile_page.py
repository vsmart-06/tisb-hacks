import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
from home_page import Home
from records import *

class Profile:
    def __init__(self, username: str):
        self.username = username
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.title("Profile")
        self.window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.window.tk.call("set_theme", "dark")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1, padx = 50)

        self.search_profile = ttk.Button(self.main_frame, text = "Search for a profile", style = "Accent.TButton", command = self.search_btn)
        self.search_profile.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.edit_profile = ttk.Button(self.main_frame, text = "Edit your profile", style = "Accent.TButton", command = self.edit_btn)
        self.edit_profile.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()

        Home(self.username)
    
    def search_btn(self):
        self.window.destroy()
        self.sub_window = tk.Tk()
        self.sub_window.title("Profile")
        self.sub_window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.sub_window.tk.call("set_theme", "dark")
        self.sub_window.geometry("700x500")
        
        self.sub_main_frame = ttk.Frame(self.sub_window)
        self.sub_main_frame.grid(row = 0, column = 1, padx = 50)

        self.search_frame = ttk.Frame(self.sub_main_frame)
        self.search_frame.grid(row = 0, column = 0)

        self.profile_ent = ttk.Entry(self.search_frame)
        self.profile_ent.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.profile_search = ttk.Button(self.sub_main_frame, text = "Search", style = "Accent.TButton", command = self.find_profile)
        self.profile_search.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.back_btn = ttk.Button(self.sub_main_frame, text = "Back", command = self.go_back)
        self.back_btn.grid(row = 2, column = 0)

        self.sub_window.update()
        self.sidebar = Sidebar(self.sub_window, self.username)

        self.sub_window.mainloop()

    def go_back(self):
        self.sub_window.destroy()
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.title("Profile")
        self.window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.window.tk.call("set_theme", "dark")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1, padx = 50)

        self.search_profile = ttk.Button(self.main_frame, text = "Search for a profile", style = "Accent.TButton", command = self.search_btn)
        self.search_profile.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.edit_profile = ttk.Button(self.main_frame, text = "Edit your profile", style = "Accent.TButton", command = self.edit_btn)
        self.edit_profile.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()

    def find_profile(self):
        user = self.profile_ent.get().strip()
        self.profile = get_profile(user)

        try:
            self.profile_frame.destroy()
        except:
            pass

        self.profile_frame = ttk.Frame(self.sub_main_frame)
        self.profile_frame.grid(row = 1, column = 0, padx = 10, pady = 10)

        if self.profile:
            self.username_lbl = ttk.Label(self.profile_frame, text = f"Username: {self.profile[0]}")
            self.username_lbl.grid(row = 0, column = 0, padx = 10, pady = 20)

            self.name_lbl = ttk.Label(self.profile_frame, text = f"Preferred name: {self.profile[1]}")
            self.name_lbl.grid(row = 1, column = 0, padx = 10, pady = 20)

            self.pno_lbl = ttk.Label(self.profile_frame, text = f"Phone number: {self.profile[2]}")
            self.pno_lbl.grid(row = 2, column = 0, padx = 10, pady = 20)

            self.email_lbl = ttk.Label(self.profile_frame, text = f"E-mail address: {self.profile[3]}")
            self.email_lbl.grid(row = 3, column = 0, padx = 10, pady = 20)
        
        else:
            self.no_user_lbl = ttk.Label(self.profile_frame, text = "No user found with that username")
            self.no_user_lbl.grid(row = 0, column = 0)

    def edit_btn(self):
        self.window.destroy()
        self.sub_window = tk.Tk()
        self.sub_window.title("Profile")
        self.sub_window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.sub_window.tk.call("set_theme", "dark")

        self.profile = get_profile(self.username)

        self.sub_main_frame = ttk.Frame(self.sub_window)
        self.sub_main_frame.grid(row = 0, column = 1)

        self.title_lbl = ttk.Label(self.sub_main_frame, text = "Your profile")
        self.title_lbl.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.profile_frame = ttk.Frame(self.sub_main_frame)
        self.profile_frame.grid(row = 1, column = 0)

        self.username_lbl_1 = ttk.Label(self.profile_frame, text = "Username: ")
        self.username_lbl_1.grid(row = 0, column = 0, padx = 10, pady = 20)
        self.username_lbl_2 = ttk.Label(self.profile_frame, text = self.profile[0])
        self.username_lbl_2.grid(row = 0, column = 1)

        self.name_lbl = ttk.Label(self.profile_frame, text = "Preferred name: ")
        self.name_lbl.grid(row = 1, column = 0, padx = 10, pady = 20)
        self.name_ent = ttk.Entry(self.profile_frame)
        self.name_ent.grid(row = 1, column = 1, padx = 10, pady = 20)
        if self.profile[1]:
            self.name_ent.insert(0, self.profile[1])

        self.pno_lbl = ttk.Label(self.profile_frame, text = "Phone number: ")
        self.pno_lbl.grid(row = 2, column = 0, padx = 10, pady = 20)
        self.pno_ent = ttk.Entry(self.profile_frame)
        self.pno_ent.grid(row = 2, column = 1, padx = 10, pady = 20)
        if self.profile[2]:
            self.pno_ent.insert(0, self.profile[2])

        self.email_lbl = ttk.Label(self.profile_frame, text = "E-mail address: ")
        self.email_lbl.grid(row = 3, column = 0, padx = 10, pady = 20)
        self.email_ent = ttk.Entry(self.profile_frame)
        self.email_ent.grid(row = 3, column = 1, padx = 10, pady = 20)
        if self.profile[3]:
            self.email_ent.insert(0, self.profile[3])
        
        self.btns_frame = ttk.Frame(self.sub_main_frame)
        self.btns_frame.grid(row = 3, column = 0, padx = 10, pady = 20)

        self.back_btn = ttk.Button(self.btns_frame, text = "Back", command = self.go_back)
        self.back_btn.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.save_btn = ttk.Button(self.btns_frame, text = "Save", style = "Accent.TButton", command = self.save_profile)
        self.save_btn.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.sub_window.update()
        self.sidebar = Sidebar(self.sub_window, self.username)

        self.sub_window.mainloop()
    
    def save_profile(self):
        try:
            self.confirmation_lbl.destroy()
        except:
            pass
        colour = "green"
        try:
            if self.pno_ent.get().strip() == "":
                text = "Changes saved"
                self.pno = "NULL"
            elif len(str(int(self.pno_ent.get().strip()))) != 10:
                text = "Your phone number can only contain 10 digits"
                colour = "red"
            else:
                self.pno = int(self.pno_ent.get().strip())
                text = "Changes saved"

        except:
            text = "Your phone number can only contain numbers"
            colour = "red"
        if colour == "green":
            edit_profile(self.username, self.name_ent.get().strip(), self.pno, self.email_ent.get().strip())
        self.confirmation_lbl = ttk.Label(self.sub_main_frame, text = text, foreground = colour)
        self.confirmation_lbl.grid(row = 4, column = 0, padx = 10, pady = 10)