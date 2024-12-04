import tkinter as tk
from tkinter import ttk, messagebox
from scraper import WebScraper

class SportOptionPage(tk.Frame):
    """Page to choose a sport."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        label = tk.Label(self, text="Choose a Sport", font=("Arial", 20))
        label.pack(pady=20)

        # Buttons options
        sports = [
            ("Basketball", "https://www.basketball-reference.com"),
            ("Baseball", "https://www.baseball-reference.com"),
            ("Hockey", "https://www.hockey-reference.com"),
        ]

        for sport_name, base_url in sports:
            button = tk.Button(
                self,
                text=f"{sport_name} Player",
                font=("Arial", 14),
                command=lambda sn=sport_name, url=base_url: self.go_to_search_page(sn, url)
            )
            button.pack(pady=10)

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
            url_ending= str(last_name[:5])+str(first_name[:2])+'01'
            print(url_ending)

            return url_ending

        


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