# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from backwise.exchange import Exchange


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BOILERPLATE                                                                        │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Boilerplate(Exchange):  # Or CCXTExchange
    """ A boilerplate class for defining new Backwise exchanges """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize exchange name
    name = ""

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH TIMEFRAMES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_timeframes(self):
        """ Fetches timeframes from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN TIMEFRAMES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_timeframes(self, timeframes):
        """ Cleans timeframes fetched from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH MARKETS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_markets(self):
        """ Fetches markets from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN MARKETS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_markets(self, markets):
        """ Cleans markets fetched from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH CURRENCIES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_currencies(self):
        """ Fetches currencies from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN CURRENCIES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_currencies(self, currencies):
        """ Cleans currencies fetched from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH TICKERS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_tickers(self, symbols):
        """ Fetches tickers from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN TICKERS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_tickers(self, tickers):
        """ Cleans tickers fetched from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH TRADING FEES                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_trading_fees(self):
        """ Fetches trading fees from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN TRADING FEES                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_trading_fees(self, trading_fees):
        """ Cleans trading fees fetched from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH OHLCV                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_ohlcv(self, symbol, timeframe, start, end):
        """ Fetches OHLCV from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN OHLCV                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_ohlcv(self, ohlcv):
        """ Cleans OHLCV fetched from an exchange """

        # NOTE: Sorting and date range trimming is already handled in the base class

        raise NotImplementedError
