import pandas as pd
import os

class WasteDatabase:
    def __init__(self, path: str = None):
        # Determine the absolute path to the data folder relative to this file [cite: 17]
        # This works on both Windows (Local) and Linux (Streamlit Cloud)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(base_dir, "data", "raw", "rectified_waste_properties.csv")
        
        # Step 1: Digital Intake (Input) [cite: 19]
        # We use the python engine to ensure compatibility across different OS
        self.df = pd.read_csv(data_path, engine='python')

    def list_waste_types(self):
        """Retrieves the list of waste types for the sidebar selectbox [cite: 19]"""
        return self.df["Waste Type"].tolist()

    def get_waste(self, name: str) -> dict:
        """Retrieves static properties like pH, Moisture, and C:N Ratio """
        row = self.df[self.df["Waste Type"] == name]
        if row.empty:
            raise ValueError(f"Waste type '{name}' not found")
        return row.iloc[0].to_dict()
