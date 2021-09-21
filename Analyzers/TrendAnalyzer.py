from typing import *

import pandas as pd
import plotly.graph_objects as go
from pandas_ta import supertrend

import Analyzers.AnalyzerInterface
from Data.Trend import Trend


class TrendAnalyzer(Analyzers.AnalyzerInterface.AnalyzerInterface):

    def __init__(self, length, multiplier):
        self.data: pd.DataFrame = None
        self.figShapes = list()
        self.trData: pd.DataFrame = None
        self.length = length
        self.multiplier = multiplier

    def start(self, data: pd.DataFrame):
        self.data = data

        trData = supertrend(high=data["high"],
                            low=data["low"],
                            close=data["low"],
                            length=self.length,
                            multiplier=self.multiplier)

        trData = trData.rename(
            columns={f"SUPERT_{self.length}_{self.multiplier}.0": "data",
                     f"SUPERTd_{self.length}_{self.multiplier}.0": "trend",
                     f"SUPERTl_{self.length}_{self.multiplier}.0": "up",
                     f"SUPERTs_{self.length}_{self.multiplier}.0": "down"})
        trData["open_time"] = data["open_time"]
        self.trData = trData

        # UP
        # upData = trData.query("up.notna()")
        self.figShapes.append(go.Scatter(x=data["open_time"], y=trData["up"],
                                         mode='lines',
                                         name='up_trend',
                                         line=dict(color="darkgreen")
                                         ))
        # DOWN
        # downData = trData.query("down.notna()")
        self.figShapes.append(go.Scatter(x=data["open_time"], y=trData["down"],
                                         mode='lines',
                                         name='down_trend',
                                         line=dict(color="red")
                                         ))

        signals = self.get_signals()

        # BUY_SIGNAL
        LongSignalsTime = list(map(lambda data: data.get_data()["open_time"],
                                   list(filter(lambda data: data.get_type() == "LONG", signals))))
        LongSignalsDataInTime = data[data["open_time"].isin(LongSignalsTime)]["close"]

        self.figShapes.append(go.Scatter(x=LongSignalsTime, y=LongSignalsDataInTime,
                                         mode='markers',
                                         name='long_signal',
                                         marker=dict(color="darkgreen",
                                                     size=10)
                                         ))

        ShortSignalsTime = list(map(lambda data: data.get_data()["open_time"],
                                    list(filter(lambda data: data.get_type() == "SHORT", signals))))

        ShortSignalsDataInTime = data[data["open_time"].isin(ShortSignalsTime)]["close"]
        self.figShapes.append(go.Scatter(x=ShortSignalsTime, y=ShortSignalsDataInTime,
                                         mode='markers',
                                         name='short_signal',
                                         marker=dict(color="red",
                                                     size=10)
                                         ))

    def get_signals(self) -> List[Trend]:
        signals = list()
        for index, row in self.trData.iterrows():
            if pd.notna(row["data"]) and row["data"] != 0.0:

                if row["trend"] != self.trData["trend"][index - 1] and row["trend"] == 1:
                    signals.append(Trend(row, "LONG"))

                if row["trend"] != self.trData["trend"][index - 1] and row["trend"] == -1:
                    signals.append(Trend(row, "SHORT"))

        return signals

    def get_trace(self) -> List[go.Scatter]:
        return self.figShapes

    def print_test(self):
        capital = 10000
        signals: List[Trend] = self.get_signals()

        long = 0
        longPrice = 0

        short = 0
        shortPrice = 0

        for signal in signals:

            deposit = capital / 100
            trend = signal.get_type()
            data = signal.get_data()

            if trend == "LONG":

                if shortPrice == 0:
                    capital -= deposit
                    long += deposit
                    longPrice = data["data"]
                else:
                    capital -= deposit
                    long += deposit
                    longPrice = data["data"]

                    capReturn = (data["data"] * deposit) / shortPrice
                    capital += capReturn
                    print(capital)
            if trend == "SHORT":

                if longPrice == 0:
                    capital -= deposit
                    short += deposit
                    shortPrice = data["data"]
                else:
                    capital -= deposit
                    short += deposit
                    shortPrice = data["data"]

                    capReturn = (data["data"] * deposit) / longPrice
                    capital += capReturn


                    print(capital)

        print(f"SUM: {capital}")
