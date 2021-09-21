from datetime import datetime

import binance as bin
import pandas as pd
from binance import ThreadedWebsocketManager

import API


class DataGenerator:

    def __init__(self, symbol, interval):
        self.client = bin.Client(API.KEY, API.PASSWORD)
        self.symbol = symbol
        self.interval = interval

        self.data = pd.DataFrame()

        self.twm = ThreadedWebsocketManager()
        self.callbacks = list()

    def start(self):
        self.__load_history()
        self.__start_beat()

    def __load_history(self):
        data = sorted(self.client.get_klines(symbol=self.symbol, interval=self.interval, limit=None),
                      key=lambda elem: elem[0])

        for candle_data in data:
            self.data = self.data.append({
                "open_time": datetime.fromtimestamp(int(candle_data[0] / 1000)),
                "open": int(float(candle_data[1])),
                "high": int(float(candle_data[2])),
                "low": int(float(candle_data[3])),
                "close": int(float(candle_data[4])),
                "volume": int(float(candle_data[5])),
                "close_time": int(float(candle_data[6])),
                "quote_asset_volume": int(float(candle_data[7])),
                "number_of_trades": int(float(candle_data[8])),
                "taker_buy_base_asset_volume": int(float(candle_data[9])),
                "taker_buy_quote_asset_volume": int(float(candle_data[10])),
            }, ignore_index=True)

    def __start_beat(self):
        self.twm.start()
        self.twm.start_kline_socket(callback=self.__call_callbacks,
                                    symbol=self.symbol,
                                    interval=self.interval)

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def __call_callbacks(self, candle_data):
        candle_data = candle_data["k"]
        self.data = self.data.append({
            "open_time": datetime.fromtimestamp(float(candle_data["t"] / 1000)),
            "open": int(float(candle_data["o"])),
            "high": int(float(candle_data["h"])),
            "low": int(float(candle_data["l"])),
            "close": int(float(candle_data["c"])),
            "volume": int(float(candle_data["v"])),
            "close time": int(float(candle_data["T"])),
            "quote_asset_volume": int(float(candle_data["q"])),
            "number_of_trades": int(float(candle_data["n"])),
            "taker_buy_base_asset_volume": int(float(candle_data["V"])),
            "taker_buy_quote_asset_volume": int(float(candle_data["Q"])),
        }, ignore_index=True)

        for func in self.callbacks:
            func(candle_data)

    def get(self) -> pd.DataFrame:
        return self.data.drop_duplicates(subset="open_time", keep="last")

    def stop(self):
        self.twm.stop()
