# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import copy

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

IS_ACTIVE = _c.IS_ACTIVE
PRECISION_AMOUNT = _c.PRECISION_AMOUNT
PRECISION_PRICE = _c.PRECISION_PRICE
TYPE = _c.TYPE


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE MARKET MIXIN                                                              │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ExchangeMarketMixin:
    """ A mixin class for handling market-related features of an exchange """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize markets cache to None
    _markets = None

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
    # │ MARKET INTERFACE                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define market interface
    interface_market = {
        IS_ACTIVE: {
            TYPE: bool,
        },
        PRECISION_AMOUNT: {TYPE: int},
        PRECISION_PRICE: {TYPE: int},
    }

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _VALIDATE MARKETS                                                              │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _validate_markets(self, markets):
        """ Validates markets fetched and cleaned from an exchange """

        # Call validate method
        return self._validate_by_interface("Market", markets, self.interface_market)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET MARKETS                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_markets(self, symbols=None):
        """ Fetches, cleans, validates, and returns markets from an exchange """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE SYMBOLS                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if symbols is a string
        if type(symbols) is str:

            # Convert symbols to list
            symbols = [symbols]

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ GET CACHED MARKETS                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get cached markets
        markets = self._markets

        # Check if markets is null
        if not markets:

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ FETCH, CLEAN, AND VALIDATE MARKETS                                     │
            # └────────────────────────────────────────────────────────────────────────┘

            # Fetch markets
            markets = self.fetch_markets()

            # Clean markets
            markets = self.clean_markets(markets)

            # Validate markets
            self._validate_markets(markets)

            # Update cached markets
            self._markets = markets

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ COPY MARKETS                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Make a deep copy of markets
        markets = copy.deepcopy(markets or {})

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ FILTER SYMBOLS                                                             │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if symbols is defined
        if symbols:

            # Filter markets
            markets = {
                symbol: info for symbol, info in markets.items() if symbol in symbols
            }

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN MARKETS                                                             │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return markets
        return markets

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET MARKET                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_market(self, symbol):
        """ Returns the market associated with a given symbol """

        # Get markets
        markets = self.get_markets(symbols=[symbol])

        # Return the market of the given symbol
        return markets.get(symbol, None)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ MARKET IS ACTIVE                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def market_is_active(self, symbol):
        """ Checks if a market symbol is active """

        # Get market
        market = self.get_market(symbol)

        # Return whether market is available
        return market is not None and market[IS_ACTIVE]
