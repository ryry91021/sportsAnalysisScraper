# Web scraping application
import requests  # HTTP requests
from bs4 import BeautifulSoup  # Soup object for HTML response
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import sys

class WebScraper:
    """Handles fetching and parsing data from sports-reference.com."""
    def __init__(self, url):
        self.url=url

    

    def fetch_data(self):
        """Verifies URL and returns soup object to retrieve the desired table"""
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return BeautifulSoup(response.content, "html.parser")

    def get_stats_table(self):
        """Extract the stats table from the HTML content."""
        soup = self.fetch_data()
        try:
            df = soup.find(id="last5")
        except Exception as e:
            print(f"Could not find last 5 game data: {e}")
            df=soup.find(id='pergame')
        if df is None:
            raise Exception("Stats table not found on the page.")
        return pd.read_html(str(df))[0]