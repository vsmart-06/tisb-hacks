import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
import os
import dotenv
import requests
from urllib import request
from PIL import Image, ImageTk
from records import *
from home_page import Home

dotenv.load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

class Lifts:
    def __init__(self, username: str):
        self.username = username

        self.window = tk.Tk()
        self.window.title("Lifts")
        self.window.tk.call("source", "./azure.tcl")
        self.window.tk.call("set_theme", "dark")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1)

        self.start_frame = ttk.Frame(self.main_frame)
        self.start_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.start_lbl = ttk.Label(self.start_frame, text = "Starting point: ")
        self.start_lbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.start_ent = ttk.Entry(self.start_frame)
        self.start_ent.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "ew")
        self.current_loc = ttk.Button(self.start_frame, text = "Current location", style = "Accent.TButton", command = self.current_location)
        self.current_loc.grid(row = 1, column = 1, padx = 10, pady = (0, 10), sticky = "ew")
        self.search_btn = ttk.Button(self.start_frame, text = "Search", command = lambda m = True: self.search_place(m))
        self.search_btn.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.end_frame = ttk.Frame(self.main_frame)
        self.end_frame.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.end_lbl = ttk.Label(self.end_frame, text = "Destination: ")
        self.end_lbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.end_ent = ttk.Entry(self.end_frame)
        self.end_ent.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "ew")
        self.search_btn = ttk.Button(self.end_frame, text = "Search", command = lambda m = False: self.search_place(m))
        self.search_btn.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.create_trip = ttk.Button(self.main_frame, text = "Create lift", style = "Accent.TButton", command = self.create_lift)
        self.create_trip.grid(row = 3, column = 0, sticky = "e", padx  = 10, pady = 30)

        self.origin = None
        self.destination = None

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()

        Home(self.username)
    
    def current_location(self):
        try:
            self.error_lbl.destroy()
        except:
            pass
        latlon = requests.post(f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}").json()["location"]

        address = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latlon['lat']},{latlon['lng']}&key={API_KEY}").json()["results"][0]["formatted_address"]

        address = ", ".join(address.split(", ")[1:])

        self.start_ent.delete(0, "end")
        self.start_ent.insert(0, address)

        self.create_map()


    def search_place(self, start: bool):
        try:
            self.error_lbl.destroy()
        except:
            pass
        if start:
            place_string = self.start_ent.get()
        else:
            place_string = self.end_ent.get()

        places = requests.get(f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={place_string}&key={API_KEY}").json()["predictions"]
        place_names = [x["description"] for x in places]
        if len(place_names) > 5:
            place_names = place_names[:5]
        
        if start:
            try:
                self.places_frame_start.destroy()
            except:
                pass
            self.places_frame_start = ttk.Frame(self.start_frame)
            self.places_frame_start.grid(row = 2, column = 1, sticky = "ew")
            self.places_btns_start = []
            for x in range(len(place_names)):
                self.places_btns_start.append(ttk.Button(self.places_frame_start, text = place_names[x], command = lambda m = x, n = True: self.choose_place(m, n)))
                self.places_btns_start[-1].grid(row = x, column = 0, pady = (0, 5), sticky = "ew")
        else:
            try:
                self.places_frame_end.destroy()
            except:
                pass
            self.places_frame_end = ttk.Frame(self.end_frame)
            self.places_frame_end.grid(row = 1, column = 1, sticky = "ew")
            self.places_btns_end = []
            for x in range(len(place_names)):
                self.places_btns_end.append(ttk.Button(self.places_frame_end, text = place_names[x], command = lambda m = x, n = False: self.choose_place(m, n)))
                self.places_btns_end[-1].grid(row = x, column = 0, pady = (0, 5), sticky = "ew")
        
        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)
    
    def choose_place(self, index, start: bool):
        try:
            self.error_lbl.destroy()
        except:
            pass
        if start:
            place = self.places_btns_start[index]["text"]
            self.start_ent.delete(0, "end")
            self.start_ent.insert(0, place)
            try:
                self.places_frame_start.destroy()
            except:
                pass
            self.origin = place
        else:
            place = self.places_btns_end[index]["text"]
            self.end_ent.delete(0, "end")
            self.end_ent.insert(0, place)
            try:
                self.places_frame_end.destroy()
            except:
                pass
            self.destination = place
        
        self.create_map()
    
    def create_map(self):
        try:
            self.error_lbl.destroy()
        except:
            pass
        origin = self.start_ent.get()
        destination = self.end_ent.get()

        if origin == "" or destination == "":
            return

        origin = requests.get(f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={origin}&key={API_KEY}").json()["predictions"][0]["description"]
        destination = requests.get(f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={destination}&key={API_KEY}").json()["predictions"][0]["description"]

        directions = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&alternatives=true&key={API_KEY}").json()

        self.routes = [x["overview_polyline"]["points"] for x in directions["routes"]]
        
        try:
            self.maps_frame.destroy()
        except:
            pass

        self.maps_frame = ttk.Frame(self.main_frame)
        self.maps_frame.grid(row = 2, column = 0)

        self.maps_lbls = []
        self.maps = []
        self.maps_select = []
        for x in range(len(self.routes)):
            self.map = f"https://maps.googleapis.com/maps/api/staticmap?size=300x300&markers=color:blue|{origin.replace(' ', '%20')}&markers=color:red|{destination.replace(' ', '%20')}&path=enc:{self.routes[x]}&key={API_KEY}"
            request.urlretrieve(self.map, f"./assets/map_route_{x}.png")

            self.maps.append(ImageTk.PhotoImage(Image.open(f"./assets/map_route_{x}.png")))
            self.maps_lbls.append(ttk.Label(self.maps_frame, image = self.maps[x]))
            self.maps_lbls[x].grid(row = 0, column = x, padx = 20, pady = 10)
            self.maps_select.append(ttk.Button(self.maps_frame, text = "Select", style = "Accent.TButton", command = lambda m = x: self.select_map(m)))
            self.maps_select[x].grid(row = 1, column = x, padx = 20, pady = (0, 10))
        
        self.origin = origin
        self.destination = destination
    
    def select_map(self, index):
        try:
            self.error_lbl.destroy()
        except:
            pass
        self.maps_frame.destroy()
        self.maps_frame = ttk.Frame(self.main_frame)
        self.maps_frame.grid(row = 2, column = 0)

        self.chosen_map = ImageTk.PhotoImage(Image.open(f"./assets/map_route_{index}.png"))
        self.chosen_index = index
        self.chosen_map_lbl = ttk.Label(self.maps_frame, image = self.chosen_map)
        self.chosen_map_lbl.grid(row = 0, column = 0)
    
    def create_lift(self):
        try:
            self.error_lbl.destroy()
        except:
            pass
        try:
            add_lift(self.username, self.origin, self.destination, self.routes[self.chosen_index])

            self.window.destroy()
            self.sub_window = tk.Tk()
            self.sub_window.title("Lifts")
            self.sub_window.tk.call("source", "./azure.tcl")
            self.sub_window.tk.call("set_theme", "dark")

            self.confirmation = ttk.Label(self.sub_window, text = f"You have successfully created a lift!\n\n\nStarting point: {self.origin}\n\nDestination: {self.destination}", justify = "center")
            self.confirmation.grid(row = 0, column = 0, padx = 10, pady = 10)
            self.chosen_map = ImageTk.PhotoImage(Image.open(f"./assets/map_route_{self.chosen_index}.png"))
            self.confirmation_map = ttk.Label(self.sub_window, image = self.chosen_map)
            self.confirmation_map.grid(row = 1, column = 0, padx = 10, pady = 10)
            self.sub_window.mainloop()

        except:
            self.error_lbl = ttk.Label(self.main_frame, text = "", foreground = "red")
            self.error_lbl.grid(row = 3, column = 0)
            if not self.origin or self.origin == "":
                self.error_lbl.config(text = "You have to input a start location")
            elif not self.destination or self.destination == "":
                self.error_lbl.config(text = "You have to input a destination")
            else:
                self.error_lbl.config(text = "You have to choose a path")