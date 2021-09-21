from pandas import DataFrame


class AnalyzerInterface:
    def start(self, data: DataFrame):
        pass

    def get_signals(self):
        pass

    def print_test(self):
        pass