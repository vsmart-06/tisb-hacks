import tkinter as tk
from tkinter import ttk
import requests
from urllib import request
import os
import dotenv
from PIL import Image, ImageTk
from sidebar import Sidebar
from records import *
from home_page import Home

dotenv.load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

class Book:
    def __init__(self, username: str):
        self.username = username

        self.window = tk.Tk()
        self.window.title("Book")
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

        self.find_btn = ttk.Button(self.main_frame, text = "Find Carpoolers", style = "Accent.TButton", command = self.find_drivers)
        self.find_btn.grid(row = 1, column = 0, pady = 30)

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()
    
    def search_place(self, pickup: bool = False):
        try:
            self.error_lbl.destroy()
        except:
            pass
        if not pickup:
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
        else:
            place_string = self.pickup_ent.get()

            places = requests.get(f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={place_string}&key={API_KEY}").json()["predictions"]
            place_names = [x["description"] for x in places]

            if len(place_names) > 5:
                place_names = place_names[:5]

            try:
                self.places_frame_start.destroy()
            except:
                pass

            self.places_frame_start = ttk.Frame(self.pickup_frame)
            self.places_frame_start.grid(row = 1, column = 1, sticky = "ew")
            self.places_btns_start = []

            for x in range(len(place_names)):
                self.places_btns_start.append(ttk.Button(self.places_frame_start, text = place_names[x], command = lambda m = x, n = True: self.choose_place(m, n)))
                self.places_btns_start[-1].grid(row = x, column = 0, pady = (0, 5), sticky = "ew")
            
            self.pickup_window.update()
            self.sidebar = Sidebar(self.pickup_window, self.username)
    
    def choose_place(self, index, pickup: bool = False):
        if not pickup:
            self.chosen_place = self.places_btns_start[index]["text"]
            self.drop_ent.delete(0, "end")
            self.drop_ent.insert(0, self.chosen_place)
            try:
                self.places_frame_start.destroy()
            except:
                pass
        else:
            self.chosen_place = self.places_btns_start[index]["text"]
            self.pickup_ent.delete(0, "end")
            self.pickup_ent.insert(0, self.chosen_place)
            try:
                self.places_frame_start.destroy()
            except:
                pass
            self.create_map()
    
    def find_drivers(self):
        try:
            self.sub_main_frame.destroy()
        except:
            if self.drop_ent.get().strip() == "":
                self.error_lbl = ttk.Label(self.main_frame, text = "Enter a destination", foreground = "red")
                self.error_lbl.grid(row = 2, column = 0, padx = 10, pady = 10)
                return
            self.window.destroy()
            self.sub_window = tk.Tk()
            self.sub_window.title("Book")
            self.sub_window.tk.call("source", "./tisb-hacks/azure.tcl")
            self.sub_window.tk.call("set_theme", "dark")

        self.sub_main_frame = ttk.Frame(self.sub_window)
        self.sub_main_frame.grid(row = 0, column = 1)

        self.maps_frame = ttk.Frame(self.sub_main_frame)
        self.maps_frame.grid(row = 0, column = 0)

        options = get_lifts()
        
        self.maps_lbls = []
        self.maps = []
        self.maps_select = []
        for x in range(len(options)):
            self.map = f"https://maps.googleapis.com/maps/api/staticmap?size=300x300&markers=color:blue|label:A|{options[x][2].replace(' ', '%20')}&markers=color:blue|label:B|{options[x][3].replace(' ', '%20')}&markers=color:red|{self.chosen_place.replace(' ', '%20')}&path=enc:{options[x][4]}&key={API_KEY}"
            request.urlretrieve(self.map, f"./tisb-hacks/assets/map_route_{x}.png")

            self.maps.append(ImageTk.PhotoImage(Image.open(f"./tisb-hacks/assets/map_route_{x}.png")))
            self.maps_lbls.append(ttk.Label(self.maps_frame, image = self.maps[x]))
            self.maps_lbls[x].grid(row = x, column = 0, padx = 20, pady = 20)
            self.maps_select.append(ttk.Button(self.maps_frame, text = "Select", style = "Accent.TButton", command = lambda m = x, n = options[x][0]: self.select_map(m, n)))
            self.maps_select[x].grid(row = x, column = 1, padx = 20, pady = (0, 10))
        
        self.sub_window.update()
        self.sidebar = Sidebar(self.sub_window, self.username)
    
    def select_map(self, index, id):
        self.chosen_index = index
        self.maps_frame.destroy()
        self.maps_frame = ttk.Frame(self.sub_main_frame)
        self.maps_frame.grid(row = 1, column = 0)

        self.data = get_lifts(id)

        distances = requests.get(f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={self.chosen_place.replace(' ', '%20')}&destinations={self.data[2].replace(' ', '%20')}|{self.data[3].replace(' ', '%20')}&mode=walking&key={API_KEY}").json()

        distances = [x["distance"]["value"] for x in distances["rows"][0]["elements"]]
        
        self.confirmation = ttk.Label(self.sub_main_frame, text = f"Details of the journey:\n\n\nStarting point (point A): {self.data[2]}\n\nDestination (point B): {self.data[3]}\n\nCarpooler: {self.data[1]}\n\nDistance of your destination from point A: {distances[0]/1000}km\nDistance of your destination from point B: {distances[1]/1000}km", justify = "center")
        self.confirmation.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.chosen_map = ImageTk.PhotoImage(Image.open(f"./tisb-hacks/assets/map_route_{index}.png"))
        self.chosen_map_lbl = ttk.Label(self.maps_frame, image = self.chosen_map)
        self.chosen_map_lbl.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.btns_frame = ttk.Frame(self.sub_main_frame)
        self.btns_frame.grid(row = 2, column = 0, padx = 10, pady = 10)

        self.confirm_btn = ttk.Button(self.btns_frame, text = "Book the ride", style = "Accent.TButton", command = self.confirm_ride)
        self.confirm_btn.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.back_btn = ttk.Button(self.btns_frame, text = "Back", command = self.find_drivers)
        self.back_btn.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.sub_window.update()
        self.sidebar = Sidebar(self.sub_window, self.username)
    
    def confirm_ride(self):
        self.sub_window.destroy()
        self.pickup_window = tk.Tk()
        self.pickup_window.title("Book")
        self.pickup_window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.pickup_window.tk.call("set_theme", "dark")

        self.pickup_main_frame = ttk.Frame(self.pickup_window)
        self.pickup_main_frame.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.pickup_frame = ttk.Frame(self.pickup_main_frame)
        self.pickup_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.pickup_lbl = ttk.Label(self.pickup_frame, text = "Enter your pickup point")
        self.pickup_lbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.pickup_ent = ttk.Entry(self.pickup_frame)
        self.pickup_ent.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.pickup_btn = ttk.Button(self.pickup_frame, text = "Search", command = lambda m = True: self.search_place(m))
        self.pickup_btn.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.map_frame = ttk.Frame(self.pickup_main_frame)
        self.map_frame.grid(row = 1, column = 0)

        self.book_btn = ttk.Button(self.pickup_main_frame, text = "Book Ride", style = "Accent.TButton", command = self.book_ride)
        self.book_btn.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.pickup_window.update()
        self.sidebar = Sidebar(self.pickup_window, self.username)
    
    def create_map(self):
        self.map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=300x300&markers=color:blue|label:A|{self.data[2].replace(' ', '%20')}&markers=color:blue|label:B|{self.data[3].replace(' ', '%20')}&markers=color:red|{self.chosen_place.replace(' ', '%20')}&path=enc:{self.data[4]}&key={API_KEY}"
        request.urlretrieve(self.map_url, f"./tisb-hacks/assets/map_route_pickup.png")

        self.map = ImageTk.PhotoImage(Image.open(f"./tisb-hacks/assets/map_route_pickup.png"))
        self.maps_lbl = ttk.Label(self.map_frame, image = self.map)
        self.maps_lbl.grid(row = 0, column = 0, padx = 20, pady = 20)
    
    def book_ride(self):
        if self.pickup_ent.get().strip() == "":
            self.error_lbl = ttk.Label(self.pickup_frame, text = "Enter a pickup location", foreground = "red")
            self.error_lbl.grid(row = 2, column = 0)
            return
        book_lift(self.data[0], self.username, self.chosen_place, self.data[1], self.data[3])
        self.pickup_window.destroy()
        self.final_window = tk.Tk()
        self.final_window.tk.call("source", "./tisb-hacks/azure.tcl")
        self.final_window.tk.call("set_theme", "dark")

        confirmation_lbl = ttk.Label(self.final_window, text = "You have successfully booked the ride.\n\nYou will receive a notification when your carpooler accepts your request and approves your pickup location.", justify = "center")
        confirmation_lbl.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.final_window.mainloop()
        Home(self.username)