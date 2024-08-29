from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, ATR
from surmount.data import Asset, OptionChain
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Focus on a preselected list of high liquidity indexes or stocks known for options trading.
        # This list can be modified based on the trader's preference or market conditions.
        self.tickers = ["SPY", "QQQ", "AAPL", "GOOGL"]
        # Assuming OptionChain can pull options data. This may require additional functionality.
        self.data_list = [OptionChain(i) for i in self.tickers]

    @property
    def interval(self):
        # Daily analysis to adjust or enter new positions
        return "1day"
    
    @property
    def assets(self):
        # Dynamic assets based on options data
        return self.tickers

    @property
    def data(self):
        # Include technical indicators in the data requirement
        return self.data_list + [ATR(i) for i in self.tickers] + [RSI(i) for i in self.tickers]
    
    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            option_chain = data[OptionChain(ticker)]
            atr = data[ATR(ticker)][-1]  # Get the last ATR value
            rsi = data[RSI(ticker)][-1]  # Get the last RSI value
            
            # Find options that expire in 30 to 60 days for selling put spreads
            candidate_options = option_chain.filter_expiration_days(30, 60)
            
            # Select options based on low RSI (suggesting oversold and potential rebound)
            # and ATR for assessing the price stability
            if rsi < 30 and atr < (atrx for atrx in data[ATR(ticker)]).mean():
                best_option = self.select_option(candidate_options, method='yield_maximizing')
                put_spread = self.create_put_spread(best_option)
                
                allocation_dict[ticker] = put_spread
        
        # In a real trading scenario, the allocations would be specific option trades rather than a simple dict
        log("Allocations for put spreads: " + str(allocation_dict))
        return TargetAllocation(allocation_dict)
    
    def select_option(self, options, method='yield_maximizing'):
        # Placeholder for selection logic based on yield maximization and risk assessment.
        # This function would analyze the available options and their spreads, implied volatility,
        # and other factors to choose the best one for selling a put spread.
        return options[0]  # Simplified for this example
        
    def create_put_spread(self, option):
        # Placeholder for creating a put spread order based on a selected option.
        # This might involve selecting the strike price for the long put based on risk tolerance, margin requirements, etc.
        return {
            'option': option.symbol,
            'spread_type': 'put',
            'action': 'sell'
        }