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

CODE = _c.CODE
PRECISION = _c.PRECISION
PRECISION_AMOUNT = _c.PRECISION_AMOUNT
PRECISION_PRICE = _c.PRECISION_PRICE
PRECISION_DISPLAY = _c.PRECISION_DISPLAY
TYPE = _c.TYPE


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE CURRENCY MIXIN                                                            │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ExchangeCurrencyMixin:
    """ A mixin class for handling currency-related features of an exchange """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize currency cache to None
    _currencies = None

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
    # │ CURRENCY INTERFACE                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define currency interface
    interface_currency = {
        PRECISION: {TYPE: int},
        PRECISION_DISPLAY: {TYPE: int},
    }

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _VALIDATE CURRENCIES                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _validate_currencies(self, currencies):
        """ Validates currencies fetched and cleaned from an exchange """

        # Call validate method
        return self._validate_by_interface(
            "Currency", currencies, self.interface_currency
        )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET CURRENCIES                                                                 │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_currencies(self, codes=None, symbols=None):
        """ Fetches, cleans, validates, and returns currencies from an exchange """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE CODES AND SYMBOLS                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if codes is a string
        if type(codes) is str:

            # Convert codes to list
            codes = [codes]

        # Check if symbols is a string
        if type(symbols) is str:

            # Convert symbols to list
            symbols = [symbols]

        # NOTE: Symbols can be passed in to alter the display precision which is
        # computed based on the markets in the exchange. If symbols are passed,
        # the resulting currencies should not be cached.

        # The symbols argument is used by methods that wish to get a display precision
        # that is relevant to a specific set of symbols, e.g. those used in a backtest

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ GET CACHED CURRENCIES                                                      │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get cached currencies
        currencies = self._currencies

        # Check if symbols are passed or currencies is null
        # NOTE: If symbols are passed, the currencies should be generated on the fly
        if symbols or not currencies:

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ FETCH AND CLEAN CURRENCIES                                             │
            # └────────────────────────────────────────────────────────────────────────┘

            # Fetch currencies
            currencies = self.fetch_currencies()

            # Clean currencies
            currencies = self.clean_currencies(currencies)

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ COMPUTE DISPLAY PRECISION                                              │
            # └────────────────────────────────────────────────────────────────────────┘

            # NOTE: This is the precision that will be used to round an amount so that
            # it is suitable for a display, e.g. in a GUI or webpage
            #   e.g. We don't need to see USDT to 6 decimal places where 2 suffices

            # This will be determined by the most common precision across markets

            # Get markets
            markets = self.get_markets(symbols=symbols)

            # Iterate over markets
            for symbol, market in markets.items():

                # Split symbol into base and quote codes
                code_base, code_quote = symbol.split("/")

                # Iterate over base and quote codes
                for code, precision_key in (
                    (code_base, PRECISION_AMOUNT),
                    (code_quote, PRECISION_PRICE),
                ):

                    # Continue if code not in currencies
                    if code not in currencies:
                        continue

                    # Get currency
                    currency = currencies[code]

                    # Get precision display counts
                    precision_display_counts = currency.setdefault(
                        PRECISION_DISPLAY, {}
                    )

                    # Get market display precision
                    precision_display = market[precision_key]

                    # Increment precision display count by 1
                    precision_display_counts[precision_display] = (
                        precision_display_counts.get(precision_display, 0) + 1
                    )

            # Iterate over currencies
            for code, currency in currencies.items():

                # Get display precision
                precision_display = currency.get(PRECISION_DISPLAY)

                # Check if display precision is null
                if not precision_display:

                    # Set display precision to precision and continue
                    currency[PRECISION_DISPLAY] = currency.get(PRECISION)
                    continue

                # Get most common display precision
                precision_display = sorted(
                    precision_display.items(), key=lambda x: x[1]
                )[-1]

                # Remove count from display precision tuple
                precision_display, _ = precision_display

                # Set final display precision
                currency[PRECISION_DISPLAY] = precision_display

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ VALIDATE AND CACHE CURRENCIES                                          │
            # └────────────────────────────────────────────────────────────────────────┘

            # Validate currencies
            self._validate_currencies(currencies)

            # Check if symbols is null
            # NOTE: We only cache currencies if no symbols are passed
            if not symbols:

                # Update cached currencies
                self._currencies = currencies

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ COPY CURRENCIES                                                            │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Make a deep copy of currencies
        currencies = copy.deepcopy(currencies or {})

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ FILTER SYMBOLS                                                             │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if codes is defined
        if codes:

            # Filter currencies
            currencies = {
                code: info for code, info in currencies.items() if code in codes
            }

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN CURRENCIES                                                          │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return currencies
        return currencies

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET CURRENCY                                                                   │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_currency(self, code, symbols=None):
        """ Returns the currency associated with a given code """

        # Get currencies
        currencies = self.get_currencies(codes=[code], symbols=symbols)

        # Return the currency of the given code
        return currencies.get(code, None)
