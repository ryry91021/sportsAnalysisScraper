import tkinter as tk
from tkinter import ttk, messagebox
from scraper import WebScraper
import os
from PIL import Image, ImageTk

from PIL import Image, ImageTk  # Pillow for resizing images
import tkinter as tk
import os

class SportOptionPage(tk.Frame):
    """Page to choose a sport."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        label = tk.Label(self, text="Choose a Sport", font=("Arial", 20))
        label.grid(row=0, column=0, columnspan=3, pady=20)  # Center title above buttons

        # Path to the images folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "images")

        # Sports data: name, URL, and image path
        sports = [
            ("Basketball", "https://www.basketball-reference.com/players/", os.path.join(images_dir, "nba_logo.png")),
            ("Baseball", "https://www.baseball-reference.com/players/", os.path.join(images_dir, "mlb_logo.png")),
            ("Hockey", "https://www.hockey-reference.com/players/", os.path.join(images_dir, "nhl_logo.png")),
        ]

        # Configure grid for centering
        self.grid_rowconfigure(1, weight=1)  # Center vertically
        self.grid_columnconfigure(0, weight=1)  # Center horizontally
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Create buttons for each sport
        for col, (sport_name, base_url, image_path) in enumerate(sports):
            # Load and resize image
            try:
                image = Image.open(image_path)
                resized_image = image.resize((100, 100), Image.Resampling.LANCZOS)
                sport_image = ImageTk.PhotoImage(resized_image)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                sport_image = None

            # Create button
            button = tk.Button(
                self,
                text=sport_name,
                font=("Arial", 14),
                image=sport_image,
                compound="top",  # Image above text
                command=lambda sn=sport_name, url=base_url: self.go_to_search_page(sn, url)
            )
            button.image = sport_image  # Prevent garbage collection
            button.grid(row=1, column=col, padx=10, pady=10)  # Place buttons side by side

    def go_to_search_page(self, sport_name, base_url):
        """Navigate to the search page with sport name and base URL."""
        search_page = self.controller.pages["SearchPage"]
        search_page.set_sport(sport_name, base_url)  # Pass data to SearchPage
        self.controller.show_page("SearchPage")


class SearchPage(tk.Frame):
    """Page to search for a player."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sport_name = None  # Name of the selected sport
        self.base_url = None    # Base URL of the selected sport

        # Title label (dynamically updated)
        self.title_label = tk.Label(self, text="", font=("Arial", 20))
        self.title_label.pack(pady=20)

        # Input field for player name
        self.player_entry = tk.Entry(self, width=40)
        self.player_entry.pack(pady=10)

        # Search button
        search_button = tk.Button(
            self,
            text="Search",
            font=("Arial", 14),
            command=self.search_player
        )
        search_button.pack(pady=10)

    def set_sport(self, sport_name, base_url):
        """Set the sport's name and base URL dynamically."""
        self.sport_name = sport_name
        self.base_url = base_url

        # Update the title label
        self.title_label.config(text=f"Search {sport_name} Player")


    def search_player(self):
        """Placeholder for player search functionality."""
        player_name = self.player_entry.get().strip()
        if not player_name:
            messagebox.showwarning("Warning", "Please enter a player's name.")
        else:
            first_name, last_name= player_name.split()
            messagebox.showinfo("Info", f"Searching for {player_name} in {self.sport_name}.")

            #For url construction to scraper.

            if len(last_name)<5:
                last_name=str(last_name)
            else:
                last_name= str(last_name[:5])

            url_ending= last_name.lower()+str(first_name[:2].lower())+'01'
            print(url_ending)
            print(self.base_url)

            if self.sport_name== 'Baseball':
                full_url=self.base_url+last_name[0].lower()+'/'+url_ending+'.shtml'
            else:    
                full_url=self.base_url+last_name[0].lower()+'/'+url_ending+'.html'
            print(full_url)

            return full_url

        


class MainApplication(tk.Tk):
    """Main application managing all pages."""

    def __init__(self):
        super().__init__()
        self.title("Sports Stats Viewer")
        self.geometry("600x400")

        # Container to hold all pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.pages = {}
        for Page in (SportOptionPage, SearchPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("SportOptionPage")

    def show_page(self, page_name):
        """Switch to the given page."""
        page = self.pages[page_name]
        page.tkraise()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()