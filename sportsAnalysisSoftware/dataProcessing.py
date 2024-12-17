from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from tkinter import messagebox
import pandas as pd


class Graph(ABC):
    """Abstract base class for creating graphs."""
    
    def __init__(self, title, x_label, y_label):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    @abstractmethod
    def plot(self, data, **kwargs):
        """Abstract method to plot the graph."""
        pass

    def setup_graph(self):
        """Common graph setup for all graphs."""
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)


class BarGraphWithSelection(Graph):
    """Singleton class for creating bar graphs with user-selected columns."""
    _instance = None  # Class-level variable to store the single instance

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of the class is created."""
        if cls._instance is None:
            cls._instance = super(BarGraphWithSelection, cls).__new__(cls)
        return cls._instance

    def __init__(self, title, x_label, y_label):
        """Initialize the bar graph with the given title and axis labels."""
        if not hasattr(self, "initialized"):  # Ensure initialization happens only once
            super().__init__(title, x_label, y_label)
            self.initialized = True  # Mark as initialized
            self.athlete_name = "Athlete"  # Default athlete name

    def set_athlete_name(self, name):
        """Set the athlete's name."""
        self.athlete_name = name
        print(name)

    def plot(self, df, **kwargs):
        """Prompt user for columns and plot the selected bar graph."""
        # Ensure all columns are numeric where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows and columns fully filled with NaNs
        df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')

        if df.empty:
            messagebox.showerror("Error", "No numerical data available after cleaning.")
            return

        # Prompt user for valid columns
        selected_columns = self.prompt_user_for_columns(df)
        if not selected_columns:
            print("No columns selected. Graph will not be generated.")
            return

        # Prepare data for the graph
        means = df[selected_columns].mean()
        x = means.index.astype(str)  # Ensure indices are strings
        y = means.values

        # Plot the bar graph
        plt.bar(x, y, color="skyblue")
        plt.title(f"{self.athlete_name}'s Selected Stats")
        self.setup_graph()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()



    def prompt_user_for_columns(self, df):
        """Prompt user to select numerical columns to include in the bar graph."""
        from tkinter import Toplevel, Checkbutton, IntVar, Button, Label, messagebox

        # Filter only numerical columns
        numerical_columns = [
            col for col in df.columns
            if pd.api.types.is_numeric_dtype(pd.to_numeric(df[col], errors="coerce"))
        ]

        if not numerical_columns:
            messagebox.showerror("Error", "No numerical columns available for selection.")
            return []

        selected_vars = {}
        selected_columns = []

        # Create a popup window
        popup = Toplevel()
        popup.title("Select Columns for Bar Graph")

        Label(popup, text="Select Columns to Include in the Graph:", font=("Arial", 12)).pack(pady=10)

        # Create checkboxes for each numerical column
        for col in numerical_columns:
            var = IntVar()
            cb = Checkbutton(popup, text=col, variable=var)
            cb.pack(anchor="w", padx=10)
            selected_vars[col] = var

        def confirm_selection():
            nonlocal selected_columns
            selected_columns = [col for col, var in selected_vars.items() if var.get()]
            popup.destroy()

        Button(popup, text="Confirm", command=confirm_selection).pack(pady=10)
        popup.wait_window()
        return selected_columns
