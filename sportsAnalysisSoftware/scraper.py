# Web scraping application
import requests  # HTTP requests
from bs4 import BeautifulSoup  # Soup object for HTML response
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import sys

from io import StringIO  # Import StringIO for wrapping HTML strings

class WebScraper:
    """Handles fetching and parsing data from sports-reference.com."""
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        """Fetches the webpage content and returns a BeautifulSoup object."""
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return BeautifulSoup(response.content, "html.parser")

    def get_stats_table(self):
        """Tries to extract the 'last5' stats table first, and falls back to 'per_game'."""
        soup = self.fetch_data()
        
        # Attempt to find the 'last5' table first
        last5_table = soup.find('table', id='last5')
        if last5_table is not None:
            print("Found 'last5' table.")
            return pd.read_html(StringIO(str(last5_table)))[0]  # Wrap in StringIO

        # Fall back to 'per_game' table if 'last5' not found
        print("'last5' table not found. Checking for 'per_game' table.")
        per_game_table = soup.find('table', id='per_game_stats')
        if per_game_table is not None:
            print("Found 'per_game' table.")
            return pd.read_html(StringIO(str(per_game_table)))[0]  # Wrap in StringIO

        # Raise an error if neither table is found
        raise Exception("Neither 'last5' nor 'per_game' stats table found on the page.")

# Test the WebScraper with the corrected implementation
url = "https://www.basketball-reference.com/players/b/brunsja01.html"
scraper = WebScraper(url)

try:
    stats_table = scraper.get_stats_table()
    print(stats_table.head())  # Display the first few rows of the table
except Exception as e:
    print(str(e))
