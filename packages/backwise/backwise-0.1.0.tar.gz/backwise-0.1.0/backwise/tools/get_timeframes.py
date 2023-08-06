# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

CHUNK = _c.CHUNK
FREQUENCY = _c.FREQUENCY
GAP = _c.GAP
LABEL = _c.LABEL

F1m = _c.F1m
F3m = _c.F3m
F5m = _c.F5m
F15m = _c.F15m
F30m = _c.F30m
F1h = _c.F1h
F2h = _c.F2h
F4h = _c.F4h
F6h = _c.F6h
F8h = _c.F8h
F12h = _c.F12h
F1d = _c.F1d
F3d = _c.F3d
F7d = _c.F7d
F28d = _c.F28d
F1M = _c.F1M
F1Y = _c.F1Y

TF1m = _c.TF1m
TF3m = _c.TF3m
TF5m = _c.TF5m
TF15m = _c.TF15m
TF30m = _c.TF30m
TF1h = _c.TF1h
TF2h = _c.TF2h
TF4h = _c.TF4h
TF6h = _c.TF6h
TF8h = _c.TF8h
TF12h = _c.TF12h
TF1d = _c.TF1d
TF3d = _c.TF3d
TF7d = _c.TF7d
TF1M = _c.TF1M


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GET TIMEFRAMES                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘


def get_timeframes():
    """ Returns a dictionary of Backwise-supported timeframes and info """

    # NOTE: These are the timeframes supported by Backwise, which may not be the same
    # as the timeframes supported by a given exchange

    # Define timeframes
    timeframes = {
        TF1m: (F1m, F1d, F1d, "One Minute"),  # 1440
        TF3m: (F3m, F1d, F1d, "Three Minutes"),  # 480
        TF5m: (F5m, F1d, F1d, "Five Minutes"),  # 288
        TF15m: (F15m, F7d, F7d, "Fifteen Minutes"),  # 672
        TF30m: (F30m, F1M, F28d, "Thirty Minutes"),  # 1460
        TF1h: (F1h, F1M, F28d, "One Hour"),  # 730
        TF2h: (F2h, F1M, F28d, "Two Hours"),  # 365
        TF4h: (F4h, F1M, F28d, "Four Hours"),  # 183
        TF6h: (F6h, F1Y, F1Y, "Six Hours"),  # 1460
        TF8h: (F8h, F1Y, F1Y, "Eight Hours"),  # 1095
        TF12h: (F12h, F1Y, F1Y, "Twelve Hours"),  # 730
        TF1d: (F1d, F1Y, F1Y, "One Day"),  # 365
        TF3d: (F3d, F1Y, F1Y, "Three Days"),  # 122
        TF7d: (F7d, F1Y, F1Y, "Seven Days"),  # 52
        TF1M: (F1M, F1Y, F1Y, "One Month"),  # 12
    }

    # Convert Backwise timeframe data to dictionary
    timeframes = {
        timeframe: {LABEL: label, FREQUENCY: frequency, CHUNK: chunk, GAP: gap}
        for timeframe, (frequency, chunk, gap, label) in timeframes.items()
    }

    # FREQUENCY: The Pandas equivalent of the timeframe

    # CHUNK: The size of the chunk in which each timeframe is stored
    #   e.g. We stuff 1 minute timeframe data into 1-day chunks in Mongo

    # GAP: The min gap between two indices that tells us our database is missing data
    #   e.g. If there is an index gap >= GAP in the df, we need to fetch from exchange

    # NOTE: We want chunks to be:
    #     1) Efficient (store a lot per chunk)
    #     2) Reasonable (not always giving way more than needed in a timeframe)
    #     Rule of thumb: max 1500 candles in a chunk

    # Return timeframes
    return timeframes


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GET TIMEFRAME INFO                                                                 │
# └────────────────────────────────────────────────────────────────────────────────────┘


def get_timeframe_info(timeframe):
    """ Returns the timeframe info of a Backwise-supported timeframe """

    # Return the timeframe info
    return get_timeframes().get(timeframe)
