# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from decimal import Decimal

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.exceptions import MissingStrategyError, MissingSymbolError


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

FEE_BUY = _c.FEE_BUY
FEE_SELL = _c.FEE_SELL
LIMIT = _c.LIMIT
ORDER_KIND_BUY = _c.ORDER_KIND_BUY
ORDER_KIND_SELL = _c.ORDER_KIND_SELL
STAKE_AMOUNT_BASE = _c.STAKE_AMOUNT_BASE
STAKE_AMOUNT_CURRENCY_CODE_BASE = _c.STAKE_AMOUNT_CURRENCY_CODE_BASE
STAKE_AMOUNT_CURRENCY_CODE_QUOTE = _c.STAKE_AMOUNT_CURRENCY_CODE_QUOTE
STAKE_AMOUNT_MIN_BASE = _c.STAKE_AMOUNT_MIN_BASE
STAKE_AMOUNT_MIN_CURRENCY_CODE_BASE = _c.STAKE_AMOUNT_MIN_CURRENCY_CODE_BASE
STAKE_AMOUNT_MIN_CURRENCY_CODE_QUOTE = _c.STAKE_AMOUNT_MIN_CURRENCY_CODE_QUOTE
STAKE_AMOUNT_MIN_QUOTE = _c.STAKE_AMOUNT_MIN_QUOTE
STAKE_AMOUNT_QUOTE = _c.STAKE_AMOUNT_QUOTE
SYMBOL_USDT = _c.SYMBOL_USDT


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BACKTEST                                                                           │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Backtest:
    """ A utility class for backtest instances """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ VERSION                                                                        │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define backtest version
    _version = 1

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ INTERFACE                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define object interface
    _interface = {
        EXCHANGE: {},
        EXCHANGE_NAME: {},
        EXCHANGE_SLUG: {},
        TIMEFRAME: {},
    }

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ HASH FIELDS                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # NOTE: Hash fields determine the identity of the backtest based on a combination
    # of field / attribute values

    # Timeframe
    # Symbols
    # Start
    # End

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ VARIANT FIELDS                                                                 │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # NOTE: Variants should fall under the same Backtest, i.e. BacktestVariant

    # Resolution
    # Currency Code Reference
    # Fee Buy
    # Fee Sell

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ TODO                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Side-wise maker or taker options for each symbol
    # Auto-fees that depend on things like maker / taker
    # Symbol-wise fees, e.g. BUSD pairs being different
    # Slippage in the case of taker
    # Missed entries in the case of maker?
    # Filter symbols in market and active (but maybe not in init)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ INIT                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __init__(
        self,
        exchange,
        timeframe,
        strategies,
        start,
        end=None,
        symbol=None,
        symbols=None,
        wallets=None,
        resolution=None,
        stake_amount_base=10,
        stake_amount_quote=10,
        stake_amount_min_base=0,
        stake_amount_min_quote=0,
        stake_amount_currency_base=None,
        stake_amount_currency_quote=None,
        stake_amount_min_currency_base=None,
        stake_amount_min_currency_quote=None,
        currency_reference=SYMBOL_USDT,
        order_kind_buy=LIMIT,
        order_kind_sell=LIMIT,
        fee_buy=None,
        fee_sell=None,
        fee_default=0.001,
        fetch_fees=True,
    ):
        """ Init Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ VALIDATE INPUTS                                                            │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if strategies is null
        if not strategies:

            # Raise MissingStrategyError
            raise MissingStrategyError(
                "At least one strategy is required for the backtest"
            )

        # Check if both symbol and symbols are null
        if not (symbol or symbols):

            # Raise MissingSymbolError
            raise MissingSymbolError("At least one symbol is required for the backtest")

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ REFERENCE CURRENCY                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize currency code reference
        currency_code_reference = currency_reference

        # NOTE: Argument omits "code" for user convenience

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ FEES                                                                       │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize fee buy
        fee_buy = fee_buy or (None if fetch_fees else fee_default)

        # Initialize fee sell
        fee_sell = fee_sell or (None if fetch_fees else fee_default)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ TIMEFRAME AND RESOLUTION                                                   │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Validate timeframe
        exchange.validate_timeframe(timeframe)

        # Initialize resolution
        resolution = resolution or timeframe

        # Validate resolution
        resolution != timeframe and exchange.validate_timeframe(resolution)

        # Enumerate timeframes
        timeframes = {tf: i for i, tf in enumerate(exchange.timeframes)}

        # Check if resolution is greater than the timeframe
        if timeframes[resolution] > timeframes[timeframe]:

            # Set resolution to timeframe
            resolution = timeframe

            # NOTE: It doesn't make sense to have lower resolution than the timeframe
            # It would be MORE data to fetch for LESS accurate exit results

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SYMBOLS                                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize symbols
        symbols = symbols or {}

        # Check if symbols is a list
        if type(symbols) is list:

            # Convert symbols to dict
            symbols = {symbol: {} for symbol in symbols}

        # Check if symbol is defined and not in symbols
        if symbol and symbol not in symbols:

            # Add symbol to the start of symbols
            # NOTE: Assuming that a single value for symbol takes precedence in order
            symbols = {**{symbol: {FEE_BUY: fee_buy, FEE_SELL: fee_sell}}, **symbols}

        # Ensure that symbols are stripped and contain one slash, e.g. BTC/USDT
        symbols = {k.strip(): v for k, v in symbols.items() if k.count("/") == 1}

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ WALLETS                                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize wallets
        wallets = wallets or {}

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ STRATEGIES                                                                 │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize strategies
        strategies = []

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE ITERABLES                                                       │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Iterate over symbols
        for symbol, info in symbols.items():

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ INITIALIZE CURRENCY CODES                                              │
            # └────────────────────────────────────────────────────────────────────────┘

            # Iterate over currency codes
            for key, currency_code in (
                (STAKE_AMOUNT_CURRENCY_CODE_BASE, stake_amount_currency_base),
                (STAKE_AMOUNT_CURRENCY_CODE_QUOTE, stake_amount_currency_quote),
                (STAKE_AMOUNT_MIN_CURRENCY_CODE_BASE, stake_amount_min_currency_base),
                (STAKE_AMOUNT_MIN_CURRENCY_CODE_QUOTE, stake_amount_min_currency_quote),
            ):

                # Get input key
                # NOTE: "code" is omitted for user convenience
                _key = key.replace("code_", "")

                # Pop currency code or get default
                # NOTE: Set explicity, or set via arg, or default to reference
                currency_code = info.pop(_key, currency_code or currency_code_reference)

                # Set currency code in info
                info[key] = info.get(key, currency_code)

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ INITIALIZE AMOUNTS                                                     │
            # └────────────────────────────────────────────────────────────────────────┘

            # Iterate over amounts
            for key, amount in (
                (STAKE_AMOUNT_BASE, stake_amount_base),
                (STAKE_AMOUNT_QUOTE, stake_amount_quote),
                (STAKE_AMOUNT_MIN_BASE, stake_amount_min_base),
                (STAKE_AMOUNT_MIN_QUOTE, stake_amount_min_quote),
            ):

                # Get amount
                amount = info.get(key, amount)

                # Convert amount to Decimal
                amount = Decimal(str(amount))

                # Set amount in info
                info[key] = amount

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ INITIALIZE FEES                                                        │
            # └────────────────────────────────────────────────────────────────────────┘

            # Iterate over fees
            for key, fee in ((FEE_BUY, fee_buy), (FEE_SELL, fee_sell)):

                # Get fee
                fee = info.get(key, None if fetch_fees else fee)

                # Check if fee is not None
                if fee is not None:

                    # Convert fee to Decimal
                    fee = Decimal(str(fee))

                # Set fee in info
                info[key] = fee

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ INITIALIZE ORDER KINDS                                                 │
            # └────────────────────────────────────────────────────────────────────────┘

            # Iterate over order kinds
            for key, order_kind in (
                (ORDER_KIND_BUY, order_kind_buy),
                (ORDER_KIND_SELL, order_kind_sell),
            ):

                # Set order kind
                info[key] = info.get(key, order_kind)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HASH                                                                       │
        # └────────────────────────────────────────────────────────────────────────────┘

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ CORE ATTRIBUTES                                                            │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Set exchange
        self.exchange = exchange

        # Set exchange slug and name
        self.exchange_name = exchange.name
        self.exchange_slug = exchange.slug

        # Set timeframe
        self.timeframe = timeframe

        # Set resolution
        self.resolution = resolution

        # Set start and end
        self.start = start
        self.end = end

        # Set wallets
        self.wallets = wallets

        # Set symbols
        self.symbols = symbols

        # Set strategies
        self.strategies = strategies

        # Set reference currency code
        self.currency_code_reference = currency_code_reference

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RESULT ATTRIBUTES                                                          │
        # └────────────────────────────────────────────────────────────────────────────┘

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ RUN                                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def run(self, interactive=False, spinner="toggle9", use_mongo=False):
        """ Runs the backtest instance with the run backtest helper function """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RUN BACKTEST                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Run backtest
        # run_backtest(
        #    backtest=self, interactive=interactive, spinner=spinner, use_mongo=use_mongo
        # )
