# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import numpy as np
import pandas as pd
import pytz

from datetime import datetime, timedelta
from decimal import Decimal

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.mixins.exchange import ExchangeMixin


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ STRATEGY                                                                           │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Strategy(ExchangeMixin):
    """ A base class for Backwise strategies """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CONSTANTS                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define constants
    #    ABOVE = ABOVE
    #    BELOW = BELOW
    #    BUY = BUY
    #    CLOSE = CLOSE
    #    HIGH = HIGH
    #    LOW = LOW
    #    OPEN = OPEN
    #    SELL = SELL
    #    SHOULD_BUY = SHOULD_BUY
    #    SHOULD_SELL = SHOULD_SELL
    #    TDELTA = TDELTA
    #    VOLUME = VOLUME
    #
    #    # Define currency constants
    #    BTC = BTC
    #    USDT = USDT

    # Define OHLCV columns
    #    OHLCV_COLUMNS_BASE = (OPEN, HIGH, LOW, CLOSE, VOLUME)  # The base OHLCV columns
    #    OHLCV_COLUMNS_SIGNAL = (SHOULD_BUY, SHOULD_SELL)  # The buy / sell signal columns

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ NAME                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize name to empty string
    name = ""

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ VARIANT                                                                        │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize variant to empty string, i.e. a "sub-name"
    # NOTE: The variant can be passed in dynamically, e.g. based on parameters
    variant = ""

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ TARGETS                                                                        │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize targets to None
    targets = None

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ STOPLOSS                                                                       │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize stoploss
    stoploss = None

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CONSOLE                                                                        │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize console
    _console = None

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ INIT METHOD                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __init__(self, *args, variant="", mongo_uri="", **kwargs):
        """ Init Method """

        # Call parent init method
        super().__init__(*args, mongo_uri=mongo_uri, **kwargs)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INSTANCE ATTRIBUTES                                                        │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Iterate over kwargs
        for key, value in kwargs.items():

            # Set instance attribute
            setattr(self, key, value)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ NAME                                                                       │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Set strategy name
        self.name = self.name or self.__class__.__name__

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ VARIANT                                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Set strategy variant, i.e. a specific version of a strategy
        self.variant = variant or self.variant

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ TARGETS                                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get targets
        targets = self.targets

        # Cast targets
        targets = {
            Decimal(str(target)): {
                self.TDELTA: pd.Timedelta(minutes=tdelta)
                if type(tdelta) is int
                else pd.Timedelta(tdelta)
            }
            for target, tdelta in targets.items()
        }

        # Sort targets favorably (ascending tdelta, descending target)
        targets = {
            target: tdelta
            for target, tdelta in sorted(
                targets.items(), key=lambda x: (x[1][self.TDELTA], -x[0])
            )
        }

        # Set targets
        self.targets = targets

        # Convert stoploss to Decimal
        self.stoploss = Decimal(str(self.stoploss)) if self.stoploss else self.stoploss

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ ADD METHOD                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __add__(self, other):
        """ Add Method """

        # Check if other is a Strategy
        if isinstance(other, Strategy):

            # Return a new strategy group
            return StrategyGroup(self.mongo_uri, self, other)

        # Raise a TypeError
        raise TypeError("Must be a Strategy instance")

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ POPULATE BUY SIGNALS                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def populate_buy_signals(self, ohlcv):
        """ Populates buy signals in a Pandas dataframe of [TS]OHLCV """

        # Set should buy column to False
        ohlcv[self.SHOULD_BUY] = False

        # Return OHLCV dataframe
        return ohlcv

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ POPULATE SELL SIGNALS                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def populate_sell_signals(self, ohlcv):
        """ Populates sell signals in a Pandas dataframe of [TS]OHLCV """

        # Set should sell column to False
        ohlcv[self.SHOULD_SELL] = False

        # Return OHLCV dataframe
        return ohlcv

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ POPULATE INDICATORS                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def populate_indicators(self, ohlcv):
        """ Populates technical indicators in a Pandas dataframe of [TS]OHLCV """

        # Return OHLCV dataframe
        return ohlcv

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _PROCESS OHLCV                                                                 │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _process_ohlcv(self, ohlcv, strategy_id=None):
        """ Processes an OHLCV dataframe for backtesting and running """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE CONSTANTS                                                       │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get column constants
        OHLCV_COLUMNS_BASE = list(Strategy.OHLCV_COLUMNS_BASE)
        OHLCV_COLUMNS_SIGNAL = list(Strategy.OHLCV_COLUMNS_SIGNAL)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SORT INDEX                                                                 │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Sort OHLCV by index for good measure
        ohlcv.sort_index(inplace=True)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ ISOLATE PREVIOUS COLUMNS                                                   │
        # └────────────────────────────────────────────────────────────────────────────┘

        # NOTE: This is done when the same OHLCV is processed under multiple strategies
        # It's nice to be able to re-use the same OHLCV data rather than copy many times
        # Isolating the previous strategy signals / indicators before computing the new
        # ones can help to reduce the possibility of column name conflicts

        # Initialize previous stragey OHLCV
        ohlcv_strategy_previous = None

        # Get previous strategy columns
        columns_strategy_previous = [
            c for c in ohlcv.columns if c not in OHLCV_COLUMNS_BASE
        ]

        # Check if previous strategy columns exist
        if columns_strategy_previous:

            # Create a new dataframe containing the previous columns only
            ohlcv_strategy_previous = ohlcv[columns_strategy_previous].copy()

            # Drop previous columns from current dataframe
            ohlcv = ohlcv.drop(columns_strategy_previous, axis=1)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ POPULATE INDICATORS                                                        │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Populate indicators in OHLCV
        self.populate_indicators(ohlcv)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ POPULATE SIGNALS                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize buy and sell signals to False
        ohlcv[OHLCV_COLUMNS_SIGNAL] = False

        # Populate buy signals
        self.populate_buy_signals(ohlcv)

        # Populate sell signals
        self.populate_sell_signals(ohlcv)

        # Set buy and sell signal columns to False if both are True
        # i.e. do nothing on contradiction
        ohlcv.loc[
            ohlcv[SHOULD_BUY] & ohlcv[SHOULD_SELL], [SHOULD_BUY, SHOULD_SELL]
        ] = False

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ ORGANIZE COLUMNS                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get OHLCV columns
        columns = list(ohlcv.columns)

        # Get indicator columns
        columns_indicator = [
            c for c in columns if c not in OHLCV_COLUMNS_BASE + OHLCV_COLUMNS_SIGNAL
        ]

        # Check if strategy ID is not None
        if strategy_id is not None:

            # Get strategy-specific columns
            columns_strategy = OHLCV_COLUMNS_SIGNAL + columns_indicator

            # Convert to rename dict
            columns_strategy = {c: f"{c}.{strategy_id}" for c in columns_strategy}

            # Add strategy ID to each column
            ohlcv.rename(columns=columns_strategy, inplace=True)

            # Convert strategy-specific columns back to renamed list
            columns_strategy = list(columns_strategy.values())

        # Check if previous strategy OHLCV is not null
        if ohlcv_strategy_previous is not None:

            # Concatenate to OHLCV
            ohlcv = pd.concat([ohlcv, ohlcv_strategy_previous], axis=1)

        # Get rearranged columns
        columns = OHLCV_COLUMNS_BASE + columns_strategy_previous + columns_strategy

        # NOTE: This ensures that the columns go
        # OHLCV + Buy + Sell + Ind. [+ Buy + Sell + Ind.] in that order to n strategies

        # Rearrange columns in dataframe
        ohlcv = ohlcv[columns]

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN PROCESSED OHLCV                                                     │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return OHLCV dataframe
        return ohlcv

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SHOULD ACT                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def should_act(
        self,
        exchange,
        symbol,
        timeframe,
        at=None,
        use_mongo=False,
    ):

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE                                                                 │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get at
        at = at or datetime.now(pytz.utc)

        # Check if exchange is a string
        if type(exchange) is str:

            # Get exchange instance
            exchange = self.get_exchange(exchange)

        # Get time delta
        tdelta = (
            pd.to_timedelta("30d" if timeframe == exchange.F1M else timeframe) * 100
        )

        # Get start as 100 periods before now
        start = at - tdelta

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ GET OHLCV                                                                  │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get OHLCV
        ohlcv = exchange.get_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            start=start,
            end=None,
            use_mongo=use_mongo,
        )

        # Remove OHLCV greater than at
        ohlcv = ohlcv[ohlcv.index <= at]

        # Process OHLCV
        ohlcv = self._process_ohlcv(ohlcv)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ DETERMINE SHOULD ACT                                                       │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get max index
        idx_max = ohlcv.index.max()

        # Initialize should buy and should sell
        should_buy = should_sell = False

        # Initialize price
        price = None

        # Get minutes
        minutes = timedelta(minutes=1)

        # Check if the difference between the latest candle and at is <= n mins
        if at - idx_max <= minutes:

            # Get the row corresponding to the max index
            row = ohlcv.loc[[idx_max]]

            # Get should buy and should sell
            should_buy, should_sell = row[SHOULD_BUY][0], row[SHOULD_SELL][0]

            # Get price
            price = Decimal(str(row[OPEN][0]))

        # Check if both should buy and should sell are True
        if should_buy and should_sell:

            # Set both to False
            should_buy = should_sell = False

        # Return should buy and should sell
        return should_buy, should_sell, price

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _DID CROSS                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _did_cross(self, series_1, series_2, direction):
        """ Creates a dataframe mask based on whether series 1 crosses series 2 """

        # Assert that direction is above or below
        assert direction in [
            self.ABOVE,
            self.BELOW,
        ], f"Direction {direction} is invalid for did_cross method"

        # Check if series 1 is a numpy array
        if isinstance(series_1, np.ndarray):

            # Convert series 1 to a Pandas series
            series_1 = pd.Series(series_1)

        # Check if series 2 is one of types that should be converted to a series
        if isinstance(series_2, (float, int, np.ndarray, np.integer, np.floating)):

            # Convert series 2 to a Pandas series
            series_2 = pd.Series(index=series_1.index, data=series_2)

        # Check if direction is above
        if direction == self.ABOVE:

            # Return series 1 crossed above series 2 mask
            return pd.Series(
                (series_1 > series_2) & (series_1.shift(1) <= series_2.shift(1))
            )

        # Otherwise check if direction is below
        elif direction == self.BELOW:

            # Return series 1 crossed below series 2 mask
            return pd.Series(
                (series_1 < series_2) & (series_1.shift(1) >= series_2.shift(1))
            )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ DID CROSS ABOVE                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def did_cross_above(self, series_1, series_2):
        """ Creates a dataframe mask on whether series 1 crosses above series 2 """

        return self._did_cross(series_1, series_2, self.ABOVE)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ DID CROSS BELOW                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def did_cross_below(self, series_1, series_2):
        """ Creates a dataframe mask on whether series 1 crosses below series 2 """

        return self._did_cross(series_1, series_2, self.BELOW)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ STRATEGY GROUP                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘


class StrategyGroup(ExchangeMixin):
    """ A utility class for housing multiple Backwise strategies """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ INIT METHOD                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __init__(self, mongo_uri, *strategies, **kwargs):
        """ Init Method """

        # Call parent init method
        super().__init__(mongo_uri=mongo_uri, **kwargs)

        # Set strategies
        self.strategies = list(strategies)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ ADD METHOD                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __add__(self, other):
        """ Add Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ STRATEGY GROUP TO STRATEGY GROUP                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Handle case of StrategyGroup
        if isinstance(other, StrategyGroup):

            # Extend the current strategy group
            self.strategies.extend(
                [s for s in other.strategies if s not in self.strategies]
            )

            # Return self
            return self

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ STRATEGY TO STRATEGY GROUP                                                 │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Otherwise handle case of strategy
        if isinstance(other, Strategy):

            # Check if the instance not already in strategy group
            if other not in self.strategies:

                # Append the instance to the currency strategy group
                self.strategies.append(other)

            # Return self
            return self

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ ALL OTHER CASES                                                            │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Raise a TypeError
        raise TypeError("Must be a StrategyGroup or Strategy instance")
