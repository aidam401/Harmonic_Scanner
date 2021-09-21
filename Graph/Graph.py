from typing import *

import plotly.graph_objects as go
from plotly.graph_objs import Figure

from Analyzers.AnalyzerInterface import AnalyzerInterface
from Data.DataGenerator import DataGenerator


class Graph:

    def __init__(self, symbol, interval):
        self.generator = DataGenerator(symbol, interval)
        self.symbol = symbol
        self.time = interval
        self.fig: Figure = None

        self.analyzers: List[AnalyzerInterface] = list()
        self.analyze: List[go.Scatter] = list()

    def load(self):
        self.generator.start()

    def get_figure(self):
        data = self.generator.get()

        self.fig = go.Figure(
            data=[go.Candlestick(
                x=data['open_time'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])
            ],

            layout=go.Layout(uirevision=True)
        )
        [self.fig.add_trace(scatter) for scatter in self.analyze]

        return self.fig

    def add_analyzer(self, analyzer):
        self.analyzers.append(analyzer)

    def start_analyze(self):
        if self.fig is None:
            self.get_figure()

        for analyzer in self.analyzers:
            analyzer.start(self.generator.get())
            scatters = analyzer.get_trace()

            analyzer.print_test() #SMAZAT

            self.analyze.extend(scatters)




    def get_actual_price(self):

        return self.generator.get().iloc[-1]["close"]
