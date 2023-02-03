import tkinter as tk
from tkinter import ttk
import requests
from urllib import request
import os
import dotenv
from PIL import Image, ImageTk
from sidebar import Sidebar
from home_page import Home
from records import *

dotenv.load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

class Notifications:
    def __init__(self, username: str):
        self.username = username
        self.window = tk.Tk()
        self.window.title("Notifications")
        self.window.tk.call("source", "./azure.tcl")
        self.window.tk.call("set_theme", "dark")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1)

        self.notifs = get_notifications(self.username)
        if self.notifs:
            self.lift = get_lifts(self.username, self.notifs[0])

        if self.notifs:
            notif_msg = ttk.Label(self.main_frame, text = self.notifs[3], justify = "center")
            notif_msg.grid(row = 0, column = 0, padx = 10, pady = 10)

            if self.notifs[4] == 0:
                self.window.protocol("WM_DELETE_WINDOW", lambda: None)
                self.map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=300x300&markers=color:blue|label:A|{self.lift[2].replace(' ', '%20')}&markers=color:blue|label:B|{self.lift[3].replace(' ', '%20')}&markers=color:red|{self.notifs[2].replace(' ', '%20')}&path=enc:{self.lift[4]}&key={API_KEY}"
                request.urlretrieve(self.map_url, f"./assets/map_route_notification.png")

                self.map = ImageTk.PhotoImage(Image.open(f"./assets/map_route_notification.png"))
                self.maps_lbl = ttk.Label(self.main_frame, image = self.map)
                self.maps_lbl.grid(row = 1, column = 0, padx = 20, pady = 20)

                distances = requests.get(f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={self.notifs[2].replace(' ', '%20')}&destinations={self.lift[2].replace(' ', '%20')}|{self.lift[3].replace(' ', '%20')}&mode=walking&key={API_KEY}").json()
                distances = [x["distance"]["value"] for x in distances["rows"][0]["elements"]]

                distance_lbl = ttk.Label(self.main_frame, text = f"Distance of pickup point from point A (starting location): {distances[0]/1000}km\nDistance of pickup point from point B (destination point): {distances[1]/1000}km")
                distance_lbl.grid(row = 2, column = 0, padx = 10, pady = 10)

                self.btns_frame = ttk.Frame(self.main_frame)
                self.btns_frame.grid(row = 3, column = 0, padx = 10, pady = 10)

                self.accept_btn = ttk.Button(self.btns_frame, text = "Accept", style = "Accent.TButton", command = lambda m = True: self.approve_notif(m))
                self.accept_btn.grid(row = 0, column = 0, padx = 10, pady = 10)
                self.decline_btn = ttk.Button(self.btns_frame, text = "Decline", command = lambda m = False: self.approve_notif(m))
                self.decline_btn.grid(row = 0, column = 1)
        
        else:
            notif_msg = ttk.Label(self.main_frame, text = "You have no notifications to view")
            notif_msg.grid(row = 0, column = 0, padx = 50, pady = 20)

        self.window.mainloop()

        Home(self.username)
    
    def approve_notif(self, approve: bool):
        if not approve:
            text = f"The user {self.username} has not approved of your pickup location at {self.lift[5]} so you cannot carpool with them :("
            remove_rider(self.lift[0])
        else:
            text = f"The user {self.username} has approved of your pickup location at {self.lift[5]} so you can carpool with them!\n\nVisit their profile to view their contact information to get in touch with them!"
        add_notification(self.lift[0], self.lift[6], self.lift[5], text, 1)
        self.window.destroy()