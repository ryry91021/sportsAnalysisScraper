from abc import ABC, abstractmethod
from PIL import Image, ImageTk  # For handling images
import tkinter as tk
from tkinter import messagebox
import os


class Page(tk.Frame, ABC):
    """Abstract base class for all pages in the application."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    @abstractmethod
    def initialize(self):
        """Initialize the page layout and widgets."""
        pass

    def navigate(self, page_name):
        """Navigate to a specific page by name."""
        self.controller.show_page(page_name)


class SportOptionPage(Page):
    """Page to choose a sport."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.initialize()

    def initialize(self):
        """Setup widgets for the sport selection page."""
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
        search_page.set_sport(sport_name, base_url)
        self.navigate("SearchPage")


class SearchPage(Page):
    """Page to search for a player."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.sport_name = None  # Name of the selected sport
        self.base_url = None    # Base URL of the selected sport
        self.initialize()

    def initialize(self):
        """Setup widgets for the player search page."""
        self.title_label = tk.Label(self, text="", font=("Arial", 20))
        self.title_label.pack(pady=20)

        self.player_entry = tk.Entry(self, width=40)
        self.player_entry.pack(pady=10)

        search_button = tk.Button(
            self,
            text="Search",
            font=("Arial", 14),
            command=self.search_player
        )
        search_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 12), fg="green")
        self.result_label.pack(pady=10)

    def set_sport(self, sport_name, base_url):
        """Set the sport's name and base URL dynamically."""
        self.sport_name = sport_name
        self.base_url = base_url
        self.title_label.config(text=f"Search {sport_name} Player")

    def search_player(self):
        """Search for the player's stats and build the URL."""
        player_name = self.player_entry.get().strip()
        if not player_name:
            messagebox.showwarning("Warning", "Please enter a player's name.")
            return

        # Split first and last name
        try:
            first_name, last_name = player_name.split()
            if len(last_name) < 5:
                last_name_url = last_name
            else:
                last_name_url = last_name[:5]

            first_name_url = first_name[:2].lower()
            url_ending = f"{last_name_url.lower()}{first_name_url}01"

            if self.sport_name == 'Baseball':
                full_url = f"{self.base_url}{last_name[0].lower()}/{url_ending}.shtml"
            else:
                full_url = f"{self.base_url}{last_name[0].lower()}/{url_ending}.html"

            self.result_label.config(text=f"URL: {full_url}")
            print(full_url)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid first and last name.")


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
