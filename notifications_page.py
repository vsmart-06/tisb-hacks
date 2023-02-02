import tkinter as tk
from tkinter import ttk
import requests
from urllib import request
import os
import dotenv
from PIL import Image, ImageTk
from sidebar import Sidebar
from records import *

dotenv.load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

class Notifications:
    def __init__(self, username: str):
        self.username = username
        self.window = tk.Tk()
        self.window.title("Notifications")
        self.window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.window.tk.call("set_theme", "dark")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1)

        self.notifs = get_notifications(self.username)
        if self.notifs:
            self.lift = get_lifts(self.notifs[0])

        if self.notifs:
            notif_msg = ttk.Label(self.main_frame, text = self.notifs[3], justify = "center")
            notif_msg.grid(row = 0, column = 0, padx = 10, pady = 10)

            self.map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=300x300&markers=color:blue|label:A|{self.lift[2]}&markers=color:blue|label:B|{self.lift[3]}&markers=color:red|{self.notifs[2]}&path=enc:{self.lift[4]}&key={API_KEY}"
            request.urlretrieve(self.map_url, f"./tisb-hacks/assets/map_route_notification.png")

            self.map = ImageTk.PhotoImage(Image.open(f"./tisb-hacks/assets/map_route_notification.png"))
            self.maps_lbl = ttk.Label(self.main_frame, image = self.map)
            self.maps_lbl.grid(row = 1, column = 0, padx = 20, pady = 20)

            self.btns_frame = ttk.Frame(self.main_frame)
            self.btns_frame.grid(row = 2, column = 0, padx = 10, pady = 10)

            self.accept_btn = ttk.Button(self.btns_frame, text = "Accept", style = "Accent.TButton")
            self.accept_btn.grid(row = 0, column = 0, padx = 10, pady = 10)
            self.decline_btn = ttk.Button(self.btns_frame, text = "Decline")
            self.decline_btn.grid(row = 0, column = 1)
        
        else:
            notif_msg = ttk.Label(self.main_frame, text = "You have no notifications to view")
            notif_msg.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()