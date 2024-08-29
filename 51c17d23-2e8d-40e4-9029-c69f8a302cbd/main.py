from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]
        self.short_window = 20
        self.long_window = 50
        self.best_ticker = None
        self.best_performance = 0

    @property
    def interval(self):
        return "30min"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        data_list = []
        for ticker in self.tickers:
            data_list #.append(Asset(ticker)) # Note: This is illustrative, Asset class usage might differ
        return data_list

    def run(self, data):
        for ticker in self.tickers:
            short_sma = SMA(ticker, data["ohlcv"], self.short_window)
            long_sma = SMA(ticker, data["ohlcv"], self.long_window)

            if len(short_sma) == 0 or len(long_sma) == 0:
                continue

            # Evaluate if the short SMA is above the long SMA, indicating a potential uptrend
            if short_sma[-1] > long_sma[-1]:
                performance = short_sma[-1] - long_sma[-1]
                if performance > self.best_performance:
                    self.best_performance = performance
                    self.best_ticker = ticker

        allocation = {ticker: 0 for ticker in self.tickers}
        if self.best_ticker:
            allocation[self.best_ticker] = 1  # Go long on the best performing stock

        # Reset for next run
        self.best_ticker = None
        self.best_performance = 0

        return TargetAllocation(allocation)