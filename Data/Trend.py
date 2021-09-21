import pandas as pd


class Trend:
    def __init__(self, data: pd.Series, type: str):
        self.data = data
        self.type = type

    def get_data(self) -> pd.Series:
        return self.data

    def get_type(self) -> str:
        return self.type

    def __str__(self):
        return f"data: {self.data.to_string}\n" \
               f"type: {self.type}\n"