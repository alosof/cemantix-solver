import pandas as pd


class Dictionary:

    def __init__(self, path: str):
        self.path = path
        self.data = self.load()

    def __getitem__(self, item):
        return self.data[item]

    def load(self):
        return pd.read_csv(self.path, sep="\t").groupby("lemme").agg({
            "freqlemfilms2": "sum",
            "freqlemlivres": "sum"
        }).reset_index()
