# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import copy

from datetime import datetime
from decimal import Decimal

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.tools import get_datetime_now_utc, is_timezone_utc


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

PRICE_ASK = _c.PRICE_ASK
PRICE_BID = _c.PRICE_BID
PRICE_MEAN = _c.PRICE_MEAN
TIMESTAMP = _c.TIMESTAMP
TYPE = _c.TYPE
VALIDATOR = _c.VALIDATOR
VOLUME_ASK = _c.VOLUME_ASK
VOLUME_BID = _c.VOLUME_BID
VOLUME_MEAN = _c.VOLUME_MEAN
VOLUME_TOTAL = _c.VOLUME_TOTAL


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE TICKER MIXIN                                                              │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ExchangeTickerMixin:
    """ A mixin class for handling ticker-related features of an exchange """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize tickers cache to None
    _tickers = None

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
    # │ TICKER INTERFACE                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define ticker interface
    interface_ticker = {
        PRICE_ASK: {
            TYPE: Decimal,
        },
        PRICE_BID: {
            TYPE: Decimal,
        },
        PRICE_MEAN: {
            TYPE: Decimal,
        },
        VOLUME_ASK: {
            TYPE: Decimal,
        },
        VOLUME_BID: {
            TYPE: Decimal,
        },
        VOLUME_MEAN: {
            TYPE: Decimal,
        },
        VOLUME_TOTAL: {
            TYPE: Decimal,
        },
        TIMESTAMP: {TYPE: datetime, VALIDATOR: lambda x: is_timezone_utc(x)},
    }

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _VALIDATE TICKERS                                                              │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _validate_tickers(self, tickers):
        """ Validates tickers fetched and cleaned from an exchange """

        # Call validate ticker method
        return self._validate_by_interface(
            "Ticker",
            tickers,
            self.interface_ticker,
        )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET TICKERS                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_tickers(self, symbols, ms=1000):
        """ Fetches, cleans, validates, and returns tickers from an exchange """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE SYMBOLS                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if symbols is a string
        if type(symbols) is str:

            # Convert to list
            symbols = [symbols]

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ GET CACHED TICKERS                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Ensure ticker cache is a dictionary
        self._tickers = self._tickers or {}

        # Get cached tickers
        tickers = self._tickers

        # Check if all symbols tickers are cached
        if all([symbol in tickers for symbol in symbols]):

            # Get UTC now
            now = get_datetime_now_utc()

            # Check if all cached tickers are up to date with respect to ms
            if all(
                [
                    (now - tickers[symbol][TIMESTAMP]).total_seconds() * 1000 <= ms
                    for symbol in symbols
                ]
            ):

                # ┌────────────────────────────────────────────────────────────────────┐
                # │ RETURN TICKERS                                                     │
                # └────────────────────────────────────────────────────────────────────┘

                # Filter tickers by symbol
                tickers = {symbol: tickers[symbol] for symbol in symbols}

                # Return a copy of the tickers
                return copy.deepcopy(tickers)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ FETCH AND CLEAN TICKERS                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Fetch tickers
        tickers = self.fetch_tickers(symbols=symbols)

        # Clean tickers
        tickers = self.clean_tickers(tickers)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ COMPUTE PRICE AND VOLUME                                                   │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Iterate over tickers
        for ticker in tickers.values():

            # Get total price
            price_total = ticker[PRICE_ASK] + ticker[PRICE_BID]

            # Add mean price
            ticker[PRICE_MEAN] = price_total / 2

            # Get total volume
            volume_total = ticker[VOLUME_ASK] + ticker[VOLUME_BID]

            # Add mean volume
            ticker[VOLUME_MEAN] = volume_total / 2

            # Add total volume
            ticker[VOLUME_TOTAL] = volume_total

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ VALIDATE TICKERS                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Validate tickers
        self._validate_tickers(tickers)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ UPDATE CACHED TICKERS                                                      │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Update cached tickers
        self._tickers.update(tickers)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ COPY AND FILTER TICKERS                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Make a deep copy of tickers
        tickers = copy.deepcopy(tickers)

        # Filter tickers by symbol
        tickers = {
            symbol: ticker for symbol, ticker in tickers.items() if symbol in symbols
        }

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN TICKERS                                                             │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return tickers
        return tickers

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET TICKER                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_ticker(self, symbol):
        """ Returns the ticker associated with a given symbol """

        # Get tickers
        tickers = self.get_tickers(symbols=[symbol])

        # Return the ticker of the given symbol
        return tickers.get(symbol, None)
