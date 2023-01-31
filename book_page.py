import tkinter as tk
from tkinter import ttk
import requests
from urllib import request
import os
import dotenv
from sidebar import Sidebar
from records import *

dotenv.load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

class Book:
    def __init__(self, username: str):
        self.username = username

        self.window = tk.Tk()
        self.window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.window.tk.call("set_theme", "dark")
        self.window.geometry("1200x400")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1, padx = 20, pady = 10)

        self.drop_frame = ttk.Frame(self.main_frame)
        self.drop_frame.grid(row = 0, column = 0)
        self.drop_lbl = ttk.Label(self.drop_frame, text = "Enter your destination: ")
        self.drop_lbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.drop_ent = ttk.Entry(self.drop_frame)
        self.drop_ent.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "ew")
        self.drop_search = ttk.Button(self.drop_frame, text = "Search", command = self.search_place)
        self.drop_search.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.find_btn = ttk.Button(self.main_frame, text = "Find Carpoolers", style = "Accent.TButton")
        self.find_btn.grid(row = 1, column = 0, pady = 30)

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()
    
    def search_place(self):
        place_string = self.drop_ent.get()

        places = requests.get(f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={place_string}&key={API_KEY}").json()["predictions"]
        place_names = [x["description"] for x in places]

        if len(place_names) > 5:
            place_names = place_names[:5]

        try:
            self.places_frame_start.destroy()
        except:
            pass

        self.places_frame_start = ttk.Frame(self.drop_frame)
        self.places_frame_start.grid(row = 1, column = 1, sticky = "ew")
        self.places_btns_start = []

        for x in range(len(place_names)):
            self.places_btns_start.append(ttk.Button(self.places_frame_start, text = place_names[x], command = lambda m = x: self.choose_place(m)))
            self.places_btns_start[-1].grid(row = x, column = 0, pady = (0, 5), sticky = "ew")
        
        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)
    
    def choose_place(self, index):
        self.chosen_place = self.places_btns_start[index]["text"]
        self.drop_ent.delete(0, "end")
        self.drop_ent.insert(0, self.chosen_place)
        try:
            self.places_frame_start.destroy()
        except:
            pass
    
    def find_drivers(self):
        self.window.destroy()

Book("vishnu")