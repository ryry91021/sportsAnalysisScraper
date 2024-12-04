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
        """Fetch HTML content from the provided URL."""
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return BeautifulSoup(response.content, "html.parser")

    def get_stats_table(self):
        """Extract the stats table from the HTML content."""
        soup = self.fetch_data()
        stats_pg = soup.find(id="per_game")
        if stats_pg is None:
            raise Exception("Stats table not found on the page.")
        return pd.read_html(str(stats_pg))[0]