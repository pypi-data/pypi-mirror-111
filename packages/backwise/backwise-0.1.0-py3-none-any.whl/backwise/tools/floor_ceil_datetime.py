# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import pandas as pd

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.tools.get_timeframes import get_timeframe_info


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

FREQUENCY = _c.FREQUENCY

F1d = _c.F1d
F1M = _c.F1M
F1Y = _c.F1Y


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ FLOOR CEIL DATETIME BY FREQUENCY                                                   │
# └────────────────────────────────────────────────────────────────────────────────────┘


def floor_ceil_datetime_by_frequency(dt, frequency):
    """ Floors and ceils a datetime object by a Pandas frequency """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ VALIDATE INPUTS                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Return datetime if datetime or frequency is null
    if not (dt and frequency):
        return dt

    # Convert datetime to Pandas datetime
    dt = pd.to_datetime(dt)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ MONTH                                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Check if frequency is month
    if frequency == F1M:

        # Return month-wise floor and ceiling=
        return (
            dt.floor(F1d) + pd.offsets.MonthBegin(-1),
            dt.ceil(F1d) + pd.offsets.MonthBegin(0),
        )

        # 2021-03-01 00:00:00 --> 2021-03-01 00:00:00
        # 2021-03-01 01:00:00 --> 2021-04-01 00:00:00

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ YEAR                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Otherwise, check if chunk size is year
    elif frequency == F1Y:

        # Return year-wise floor and ceiling=
        return (
            dt.floor(F1d) + pd.offsets.YearBegin(-1),
            dt.ceil(F1d) + pd.offsets.YearBegin(0),
        )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GENERAL CASE                                                                   │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Return general floor and ceiling=
    return (dt.floor(frequency), dt.ceil(frequency))


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ FLOOR DATETIME BY FREQUENCY                                                        │
# └────────────────────────────────────────────────────────────────────────────────────┘


def floor_datetime_by_frequency(dt, frequency):
    """ Floors a datetime object by a Pandas frequency """

    # Get floor and ceiling
    floor, _ = floor_ceil_datetime_by_frequency(dt, frequency)

    # Return floor
    return floor


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CEIL DATETIME BY FREQUENCY                                                         │
# └────────────────────────────────────────────────────────────────────────────────────┘


def ceil_datetime_by_frequency(dt, frequency):
    """ Ceils a datetime object by a Pandas frequency """

    # Get floor and ceiling
    _, ceil = floor_ceil_datetime_by_frequency(dt, frequency)

    # Return ceiling
    return ceil


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ FLOOR CEIL DATETIME BY TIMEFRAME                                                   │
# └────────────────────────────────────────────────────────────────────────────────────┘


def floor_ceil_datetime_by_timeframe(dt, timeframe):
    """ Floors and ceils a datetime object by an OHLCV timeframe """

    # Get timeframe info
    timeframe_info = get_timeframe_info(timeframe)

    # Get frequency
    frequency = timeframe_info[FREQUENCY] if timeframe_info else None

    # Return floor and ceiling of datetime based on frequency
    return floor_ceil_datetime_by_frequency(dt, frequency)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ FLOOR DATETIME BY TIMEFRAME                                                        │
# └────────────────────────────────────────────────────────────────────────────────────┘


def floor_datetime_by_timeframe(dt, timeframe):
    """ Floors a datetime object by an OHLCV timeframe """

    # Get floor and ceiling
    floor, _ = floor_ceil_datetime_by_timeframe(dt, timeframe)

    # Return floor
    return floor


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CEIL DATETIME BY TIMEFRAME                                                         │
# └────────────────────────────────────────────────────────────────────────────────────┘


def ceil_datetime_by_timeframe(dt, timeframe):
    """ Ceils a datetime object by an OHLCV timeframe """

    # Get floor and ceiling
    _, ceil = floor_ceil_datetime_by_timeframe(dt, timeframe)

    # Return ceiling
    return ceil
