# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import copy

from decimal import Decimal

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

MAKER = _c.MAKER
TAKER = _c.TAKER
TYPE = _c.TYPE


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE TRADE MIXIN                                                               │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ExchangeTradeMixin:
    """ A mixin class for handling trade-related features of an exchange """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize trading fees cache to None
    _trading_fees = None

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
    # │ TRADING FEE INTERFACE                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define trading fee interface
    interface_trading_fee = {
        MAKER: {TYPE: Decimal},
        TAKER: {TYPE: Decimal},
    }

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _VALIDATE TRADING FEES                                                         │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _validate_trading_fees(self, trading_fees):
        """ Validates trading fees fetched and cleaned from an exchange """

        # Call validate method
        return self._validate_by_interface(
            "Trading Fee", trading_fees, self.interface_trading_fee
        )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET TRADING FEES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_trading_fees(self, symbols=None, maker=False, taker=False):
        """ Fetches, cleans, validates, and returns trading fees from an exchange """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE SYMBOLS                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if symbols is a string
        if type(symbols) is str:

            # Convert symbols to list
            symbols = [symbols]

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ GET CACHED TRADING FEES                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get cached trading fees
        trading_fees = self._trading_fees

        # Check if trading fees is null
        if not trading_fees:

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ FETCH, CLEAN, AND VALIDATE TRADING FEES                                │
            # └────────────────────────────────────────────────────────────────────────┘

            # Fetch trading fees
            trading_fees = self.fetch_trading_fees()

            # Clean trading fees
            trading_fees = self.clean_trading_fees(trading_fees)

            # Validate trading fees
            self._validate_trading_fees(trading_fees)

            # Update cached trading fees
            self._trading_fees = trading_fees

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ COPY TRADING FEES                                                          │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Make a deep copy of trading fees
        trading_fees = copy.deepcopy(trading_fees or {})

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ FILTER SYMBOLS                                                             │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if symbols is defined
        if symbols:

            # Filter trading fees
            trading_fees = {
                symbol: info
                for symbol, info in trading_fees.items()
                if symbol in symbols
            }

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ FILTER TYPES                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if maker or taker
        if maker is True or taker is True:

            # Get key
            key = MAKER if maker else TAKER

            # Filter maker fees
            trading_fees = {symbol: info[key] for symbol, info in trading_fees.items()}

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN TRADING FEES                                                        │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return trading fees
        return trading_fees

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET TRADING FEE                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_trading_fee(self, symbol, maker=False, taker=False):
        """ Returns the trading fee associated with a given symbol """

        # Get trading fees
        trading_fees = self.get_trading_fees(symbols=[symbol], maker=maker, taker=taker)

        # Return the trading fee of the given symbol
        return trading_fees.get(symbol, None)
