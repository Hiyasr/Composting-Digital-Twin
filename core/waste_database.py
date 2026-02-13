import pandas as pd

class WasteDatabase:
    def __init__(self, path: str):
        # The file is a CSV, so we must use read_csv
        self.df = pd.read_csv(r"C:\Users\hiyas\OneDrive\Desktop\epics-digital-compost-ai\data\raw\rectified_waste_properties.csv")

    def list_waste_types(self):
        return self.df["Waste Type"].tolist()

    def get_waste(self, name: str) -> dict:
        row = self.df[self.df["Waste Type"] == name]
        if row.empty:
            raise ValueError(f"Waste type '{name}' not found")
        return row.iloc[0].to_dict()