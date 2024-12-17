import requests  # HTTP requests
from bs4 import BeautifulSoup  # Soup object for HTML response
import pandas as pd
from io import StringIO

class WebScraper:
    """Handles fetching and parsing data from sports-reference.com."""
    def __init__(self, url, sport):
        self.url = url
        self.sport = sport

    def fetch_data(self):
        """Fetches the webpage content and returns a BeautifulSoup object."""
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return BeautifulSoup(response.content, "html.parser")

    def get_stats_table(self):
        """Extracts specific stats for Baseball or Basketball."""
        soup = self.fetch_data()
        
        if self.sport == "Basketball":
            return self._handle_basketball(soup)
        elif self.sport == "Baseball":
            return self._handle_baseball(soup)
        elif self.sport=="Hockey":
            return self._handle_hockey(soup)
        else:
            raise Exception("Unsupported sport!")

    def _handle_basketball(self, soup):
        """Handles Basketball: Extract 'last5' or 'per_game' tables."""
        last5_table = soup.find('table', id='last5')
        if last5_table:
            print("Found 'last5' table.")
            return pd.read_html(StringIO(str(last5_table)))[0]

        print("'last5' table not found. Checking for 'per_game' table.")
        per_game_table = soup.find('table', id='per_game_stats')
        if per_game_table:
            print("Found 'per_game' table.")
            df=pd.read_html(StringIO(str(per_game_table)))[0]
            df.drop('Age', axis=1, inplace=True)
            return df

        raise Exception("Neither 'last5' nor 'per_game' stats table found on the page.")

    def _handle_baseball(self, soup):
        """Handles Baseball: Extract stats from batting table."""
        batting_table = soup.find('table', id='players_standard_batting')
        

        if batting_table:
            print("Found 'players_standard_batting' table.")
            batting_df = pd.read_html(StringIO(str(batting_table)))[0]
            batting_df = batting_df[['Season', 'WAR', 'AB', 'H', 'HR', 'BA', 'R', 'RBI', 'SB']]
            return batting_df

        elif not batting_table:
            pitching_table=soup.find('table', id='players_standard_pitching')
            pitching_df=pd.read_html(StringIO(str(pitching_table)))[0]
            pitching_df=pitching_df[['IP', 'H', 'R', 'ER', 'HR', 'SO', 'HBP', 'BK', 'BF']]
            return pitching_df
        else:
            raise Exception("Tables Not found.")
        
    def _handle_hockey(self, soup):
        """Handles Hockey: Extract 'last5' stats table and clean data."""
        last5 = soup.find('table', id='last5')
        goalie_stats = soup.find('table', id='goalie_stats')
        player_stats = soup.find('table', id='player_stats')
        
        # Step 1: Handle 'last5' table (current players)
        if last5:
            print("Found 'last5' table.")
            df = pd.read_html(StringIO(str(last5)), header=[0, 1])[0]
            return self._clean_hockey_dataframe(df)
        
        # Step 2: Check 'goalie_stats' table (goalies)
        if goalie_stats:
            print("Found 'goalie_stats' table.")
            df = pd.read_html(StringIO(str(goalie_stats)), header=[0, 1])[0]
            if not df.dropna().empty:  # Ensure the table has meaningful data
                return self._clean_hockey_dataframe(df)
            else:
                print("'goalie_stats' table is empty. Checking 'player_stats'...")

        # Step 3: Handle 'player_stats' table (retired players)
        if player_stats:
            print("Found 'player_stats' table.")
            df = pd.read_html(StringIO(str(player_stats)), header=[0, 1])[0]
            return self._clean_hockey_dataframe(df)

        # Raise an exception if no valid table is found
        raise Exception("No valid hockey stats table found.")

    def _clean_hockey_dataframe(self, df):
        """Cleans up the hockey stats DataFrame."""
        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [' '.join(col).strip() for col in df.columns.values]
        # Remove rows that are not numeric (like extra header rows)
        if df.iloc[0].apply(lambda x: isinstance(x, str) and "Scoring" in x).any():
            df = df.iloc[1:].reset_index(drop=True)
        # Ensure all data is numeric where possible
        df = df.apply(pd.to_numeric, errors='coerce')
        # Drop fully empty columns
        return df.dropna(axis=1, how="all")
