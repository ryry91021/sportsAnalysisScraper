from abc import ABC, abstractmethod
from PIL import Image, ImageTk  # For handling images
import tkinter as tk
from tkinter import messagebox, ttk
import os
from scraper import *
from dataProcessing import *


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
        """Search for the player's stats and navigate to DataDisplayPage."""
        player_name = self.player_entry.get().strip()
        if not player_name:
            messagebox.showwarning("Warning", "Please enter a player's name.")
            return

        try:
            # Split player name into first and last
            first_name, last_name = player_name.split()

            # Construct the player's specific URL
            if len(last_name) < 5:
                last_name_part = last_name.lower()
            else:
                last_name_part = last_name[:5].lower()

            first_name_part = first_name[:2].lower()
            player_url_ending = f"{last_name_part}{first_name_part}01"

            # Adjust URL based on sport
            if self.sport_name == 'Baseball':
                full_url = f"{self.base_url}{last_name[0].lower()}/{player_url_ending}.shtml"
            else:  # For Basketball and Hockey
                full_url = f"{self.base_url}{last_name[0].lower()}/{player_url_ending}.html"

            print(f"Constructed URL: {full_url}")  # Debugging

            # Pass the constructed URL to the WebScraper
            scraper = WebScraper(full_url)
            df = scraper.get_stats_table()

            # Pass DataFrame to DataDisplayPage
            data_display_page = self.controller.pages["DataDisplayPage"]
            data_display_page.display_dataframe(df)

            # Navigate to DataDisplayPage
            self.navigate("DataDisplayPage")
        except ValueError:
            messagebox.showerror("Error", "Please enter both first and last name.")
        except Exception as e:
            messagebox.showerror("Error", str(e))



class DataDisplayPage(Page):
    """Page to display player statistics and allow graph creation."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        print("DataDisplayPage: Initializing...")  # Debugging
        self.initialize()  # Ensure this is called to set up widgets

    def initialize(self):
        """Setup the layout with a plain text display and a graph button."""
        print("Initializing DataDisplayPage...")  # Debugging

        # Title
        self.title_label = tk.Label(self, text="Player Statistics", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Add plain text display for DataFrame
        self.text_display = tk.Text(self, wrap="none", height=15, font=("Courier", 10))
        self.text_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Add "Create Bar Graph" button
        print("Adding Create Bar Graph button...")  # Debugging
        self.graph_button = tk.Button(
            self,
            text="Create Bar Graph",
            font=("Arial", 14),
            command=self.create_bar_graph  # Function to generate the graph
        )
        self.graph_button.pack(pady=10)
        print("Graph Button added and packed.")  # Debugging

    def display_dataframe(self, df):
        """Display the DataFrame as plain text in the UI."""
        self.df = df  # Save the DataFrame for graph creation

        # Update plain text display
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", df.to_string(index=False))

    def create_bar_graph(self):
        """Trigger the bar graph creation process."""
        if not hasattr(self, "df") or self.df.empty:
            messagebox.showerror("Error", "No data available to create a graph.")
            return

        graph = BarGraphWithSelection(
            title="Selected Numerical Stats",
            x_label="Index",
            y_label="Values"
        )
        graph.plot(self.df)



class MainApplication(tk.Tk):
    """Main application managing all pages."""
    def __init__(self):
        super().__init__()
        self.title("Sports Stats Viewer")
        self.geometry("800x600")

        # Container for pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.pages = {}
        for Page in (SportOptionPage, SearchPage, DataDisplayPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("SportOptionPage")

    def show_page(self, page_name):
        """Switch to the specified page."""
        page = self.pages[page_name]
        page.tkraise()



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
