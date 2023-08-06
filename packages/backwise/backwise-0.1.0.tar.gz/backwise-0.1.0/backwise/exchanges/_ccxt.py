# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import ccxt

from ccxt.base.errors import AuthenticationError

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.exchange import Exchange
from backwise.tools import to_datetime_utc, to_decimal


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

API = _c.API
CODE = _c.CODE
IS_ACTIVE = _c.IS_ACTIVE
MAKER = _c.MAKER
PRECISION = _c.PRECISION
PRECISION_AMOUNT = _c.PRECISION_AMOUNT
PRECISION_PRICE = _c.PRECISION_PRICE
PRICE_ASK = _c.PRICE_ASK
PRICE_BID = _c.PRICE_BID
SECRET = _c.SECRET
TAKER = _c.TAKER
TIMEOUT = _c.TIMEOUT
TIMESTAMP = _c.TIMESTAMP
VOLUME_ASK = _c.VOLUME_ASK
VOLUME_BID = _c.VOLUME_BID


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CCXT EXCHANGE                                                                      │
# └────────────────────────────────────────────────────────────────────────────────────┘


class CCXTExchange(Exchange):
    """ A base class for Backwise exchanges that use CCXT under the hood """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ INIT METHOD                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __init__(self, *args, **kwargs):
        """ Init Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE PARENT                                                          │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Call parent init method
        super().__init__(*args, **kwargs)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ CONSTANTS                                                                  │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Define API key
        APIKEY = "apiKey"

        # Define rate limit
        RATE_LIMIT = "rateLimit"
        ENABLE_RATE_LIMIT = "enableRateLimit"

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ CCXT INSTANCES                                                             │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get exchange ID
        exchange_id = self.slug

        # Get exchange class
        ExchangeClass = getattr(ccxt, exchange_id)

        # Define exchange kwargs
        exchange_kwargs = {TIMEOUT: self.timeout_ms, ENABLE_RATE_LIMIT: True}

        # Initialize read instance
        self.ccxt_read = ExchangeClass(
            {
                APIKEY: self.api_key_read,
                SECRET: self.api_secret_read,
                RATE_LIMIT: 400,
                **exchange_kwargs,
            }
        )

        # Initialize trade instance
        self.ccxt_trade = ExchangeClass(
            {
                APIKEY: self.api_key_trade,
                SECRET: self.api_secret_trade,
                RATE_LIMIT: 200,  # Shorter rate limits
                **exchange_kwargs,
            }
        )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH TIMEFRAMES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_timeframes(self):
        """ Fetches timeframes from an exchange """

        # Return CCXT timeframes dict
        return self.ccxt_read.timeframes

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN TIMEFRAMES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_timeframes(self, timeframes):
        """ Cleans timeframes fetched from an exchange """

        # Return timeframes
        return {timeframe: {API: api} for timeframe, api in timeframes.items()}

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH MARKETS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_markets(self):
        """ Fetches markets from an exchange """

        # Fetch and return markets
        return self.ccxt_read.load_markets()

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN MARKETS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_markets(self, markets):
        """ Cleans a markets fetched from an exchange """

        # Initialize cleaned markets
        cleaned_markets = {}

        # Iterate over markets
        for symbol, market in markets.items():

            # Construct cleaned market
            cleaned_market = {
                IS_ACTIVE: market["active"],
                PRECISION_AMOUNT: market["precision"]["amount"],
                PRECISION_PRICE: market["precision"]["price"],
            }

            # Add cleaned market to cleaned markets
            cleaned_markets[symbol] = cleaned_market

        # Return cleaned markets
        return cleaned_markets

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH CURRENCIES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_currencies(self):
        """ Fetches currencies from an exchange """

        # Get markets
        # NOTE: This will call ccxt.load_markets() if necessary, and populate currencies
        self.get_markets()

        # Return currencies
        return self.ccxt_read.currencies

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN CURRENCIES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_currencies(self, currencies):
        """ Cleans currencies fetched from an exchange """

        # Initialize cleaned currencies
        cleaned_currencies = {}

        # Iterate over currencies
        for code, currency in currencies.items():

            # Construct cleaned currency
            cleaned_currency = {PRECISION: currency["precision"]}

            # Add cleaned currency to cleaned currencies
            cleaned_currencies[code] = cleaned_currency

        # Return cleaned currencies
        return cleaned_currencies

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH TICKERS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_tickers(self, symbols):
        """ Fetches tickers from an exchange """

        # Fetch and return tickers
        return self.ccxt_read.fetch_tickers(symbols)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN TICKERS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_tickers(self, tickers):
        """ Cleans tickers fetched from and exchange """

        # Initialize cleaned tickers
        cleaned_tickers = {}

        # Iterate over tickers
        for symbol, ticker in tickers.items():

            # Construct cleaned ticker
            cleaned_ticker = {
                PRICE_ASK: to_decimal(ticker["ask"]),
                PRICE_BID: to_decimal(ticker["bid"]),
                VOLUME_ASK: to_decimal(ticker["askVolume"]),
                VOLUME_BID: to_decimal(ticker["bidVolume"]),
                TIMESTAMP: to_datetime_utc(ticker["timestamp"], unit_ms=True),
            }

            # Add cleaned ticker to cleaned tickers
            cleaned_tickers[symbol] = cleaned_ticker

        # Return cleaned tickers
        return cleaned_tickers

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH TRADING FEES                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_trading_fees(self):
        """ Fetches trading fees from an exchange """

        # Check if read API key and secret are defined
        if self.api_key_read and self.api_secret_read:

            # Initialize try-except block
            try:

                # Fetch and return trading fees from private API
                return self.ccxt_read.fetch_trading_fees()

            # Pass in case of invalid credentials
            except AuthenticationError:
                pass

        # Get markets
        self.get_markets()

        # Return the CCXT instance's markets
        return self.ccxt_read.markets

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN TRADING FEES                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_trading_fees(self, trading_fees):
        """ Cleans trading fees fetched from an exchange """

        # Initialize cleaned trading fees
        cleaned_trading_fees = {}

        # Iterate over trading fees
        for symbol, trading_fee in trading_fees.items():

            # Construct cleaned trading fee
            cleaned_trading_fee = {
                MAKER: to_decimal(trading_fee["maker"]),
                TAKER: to_decimal(trading_fee["taker"]),
            }

            # Add cleaned trading fee to cleaned trading fees
            cleaned_trading_fees[symbol] = cleaned_trading_fee

        # Return cleaned trading fees
        return cleaned_trading_fees

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH OHLCV                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_ohlcv(self, symbol, timeframe, start, end):
        """ Fetches OHLCV from an exchange """

        # Convert start and end datetimes into a timestamp in milliseconds
        start, end = [int(dt.timestamp() * 1000) for dt in (start, end)]

        # Initialize OHLCV
        ohlcv = []

        # Initialize while loop
        while start <= end:

            # Fetch new OHLCV
            new_ohlcv = self.ccxt_read.fetch_ohlcv(
                symbol=symbol, timeframe=timeframe, since=start
            )

            # Break if new OHLCV is null
            if not new_ohlcv:
                break

            # Extend OHLCV by new OHLCV
            ohlcv += new_ohlcv

            # Get last candle (second to last just for good measure)
            last_candle = new_ohlcv[-2] if len(new_ohlcv) > 1 else new_ohlcv[-1]

            # Get timestamp to last candle as the new start
            new_start = last_candle[0]

            # Break if new start is equal to the previous start
            if new_start == start:
                break

            # Set start to new start
            start = new_start

        # Return OHLCV
        return ohlcv

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN OHLCV                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_ohlcv(self, ohlcv):
        """ Cleans OHLCV fetched from an exchange """

        # Ensure that the OHLCV data is unique
        ohlcv = list(set(tuple(o) for o in ohlcv))

        # Convert the OHLCV data into appropriate types
        ohlcv = [
            (
                to_datetime_utc(t, unit_ms=True),
                to_decimal(o),
                to_decimal(h),
                to_decimal(l),
                to_decimal(c),
                to_decimal(v),
            )
            for (t, o, h, l, c, v) in ohlcv
        ]

        # Return cleaned OHLCV
        return ohlcv
