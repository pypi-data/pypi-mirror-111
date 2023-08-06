# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import pandas as pd

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from backwise.tools.floor_ceil_datetime import (
    ceil_datetime_by_frequency,
    floor_datetime_by_frequency,
)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GET CHUNK RANGE                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘


def get_chunk_range(start, end, frequency, chunk):

    # Get floor of start as chunk start
    chunk_start = floor_datetime_by_frequency(start, chunk)

    # Get ceiling of end as chunk end
    chunk_end = ceil_datetime_by_frequency(end, chunk)

    # Reduce the chunk end by one frequency
    chunk_end = chunk_end - pd.to_timedelta(frequency)

    # NOTE: This is done to prevent writing partials to the next Arctic chunk
    # since chunks are replaced atomically on write. The Pandas ceiling alone
    # spans into the next Arctic chunk.

    # Example:
    # Pandas ceiling of 2021-05-31 23:30 --> 2021-06-01 00:00 @ 1m chunked by 1D
    # Arctic ceiling of 2021-05-31 23:30 --> 2021-05-31 23:59 @ 1m chunked by 1D

    # Check if end is greater than chunk end
    # NOTE: This happens when Arctic ceiling < end <= Pandas ceiling
    if end > chunk_end:

        # Add one frequency to end
        end = end + pd.to_timedelta(frequency)

        # Add one frequency to end and then re-compute chunk end
        chunk_end = ceil_datetime_by_frequency(end, chunk) - pd.to_timedelta(frequency)

    # Return chunk start and chunk end
    return chunk_start, chunk_end
