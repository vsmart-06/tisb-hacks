import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
import os
import dotenv
import requests
from urllib import request
from PIL import Image, ImageTk

dotenv.load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

class Home:
    def __init__(self, username: str):
        self.window = tk.Tk()
        self.window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.window.tk.call("set_theme", "dark")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1)

        self.map_title = ttk.Label(self.main_frame, text = "Your location")
        self.map_title.grid(row = 0, column = 0, pady = 20, padx = (20, 10))
        latlon = requests.post(f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}").json()["location"]
        self.map = f"https://maps.googleapis.com/maps/api/staticmap?center={latlon['lat']},{latlon['lng']}&size=500x500&zoom=15&markers=color:red|{latlon['lat']},{latlon['lng']}&key={API_KEY}"
        request.urlretrieve(self.map, "./tisb-hacks/map.png")
        self.img = ImageTk.PhotoImage(Image.open("./tisb-hacks/map.png"))
        self.map_lbl = ttk.Label(self.main_frame, image = self.img)
        self.map_lbl.grid(row = 1, column = 0, padx = 20, pady = (10, 20))

        self.window.update()
        self.sidebar = Sidebar(self.window, username)

        self.window.mainloop()