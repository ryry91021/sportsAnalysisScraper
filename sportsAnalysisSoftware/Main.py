import tkinter as tk
from scraper import WebScraper
from dataProcessing import BarGraphWithSelection
from interface  import SportOptionPage, SearchPage, DataDisplayPage  # Import your pages

class MainApplication(tk.Tk):
    """Main driver class for the sports stats viewer application."""
    def __init__(self):
        super().__init__()

        self.title("Sports Stats Viewer")
        self.geometry("800x600")  # Set default window size

        # Container to hold pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary to hold all pages
        self.pages = {}
        for PageClass in (SportOptionPage, SearchPage, DataDisplayPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("SportOptionPage")  # Start on the sport selection page

    def show_page(self, page_name):
        """Display a page by name."""
        page = self.pages[page_name]
        page.tkraise()  # Bring the specified page to the front


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
