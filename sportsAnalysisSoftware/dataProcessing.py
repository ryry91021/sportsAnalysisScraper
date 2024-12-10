from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class Graph(ABC):
    """Abstract base class for creating graphs."""
    
    def __init__(self, title, x_label, y_label):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    @abstractmethod
    def plot(self, data, **kwargs):
        """Abstract method to plot the graph. Must be implemented by subclasses."""
        pass

    def setup_graph(self):
        """Common graph setup for all graphs."""
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)


class BarGraphWithSelection(Graph):
    """Concrete class for creating bar graphs with user-selected columns."""
    def __init__(self, title, x_label, y_label):
        super().__init__(title, x_label, y_label)

    def plot(self, df, **kwargs):
        """Prompt user for columns and plot the selected bar graph."""
        selected_columns = self.prompt_user_for_columns(df)  # Pass the df
        if not selected_columns:
            print("No columns selected. Graph will not be generated.")
            return

        # Prepare data for the graph
        means = df[selected_columns].mean()  # Calculate the mean of each selected column
        x = means.index  # Column names for the x-axis
        y = means.values  # Mean values for the y-axis

        plt.bar(x, y, color="skyblue")
        self.setup_graph()
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.show()

    def prompt_user_for_columns(self, df):
        """Prompt user to select numerical columns to include in the bar graph."""
        from tkinter import Toplevel, Checkbutton, IntVar, Button, Label

        numerical_columns = df.select_dtypes(include=["number"]).columns
        if numerical_columns.empty:
            print("No numerical columns available for selection.")
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
            cb.pack(anchor="w", padx=20)
            selected_vars[col] = var

        # Confirm selection
        def confirm_selection():
            nonlocal selected_columns
            selected_columns = [col for col, var in selected_vars.items() if var.get()]
            print(f"Selected columns: {selected_columns}")  # Debug
            popup.destroy()

        Button(popup, text="Confirm", command=confirm_selection).pack(pady=10)

        popup.wait_window()  # Wait for the user to close the popup
        return selected_columns
