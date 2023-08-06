# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import pandas as pd
import pytz
import time

from arctic import Arctic, CHUNK_STORE
from arctic.date import DateRange
from datetime import datetime, timedelta

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.exceptions import InvalidTimezoneError
from backwise.tools import get_chunk_range, get_datetime_now_utc, is_timezone_utc


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

CHUNK = _c.CHUNK
DATE = _c.DATE
EXCHANGE_READ = _c.EXCHANGE_READ
FREQUENCY = _c.FREQUENCY
GAP = _c.GAP
MONGO_READ = _c.MONGO_READ
MONGO_WRITE = _c.MONGO_WRITE
TIMESTAMP = _c.TIMESTAMP
TOTAL = _c.TOTAL


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE OHLCV MIXIN                                                               │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ExchangeOHLCVMixin:
    """ A mixin class for handling fetching and processing of OHLCV data """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH OHLCV                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_ohlcv(self, symbol, timeframe, start, end):
        """ Fetches OHLCV from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN OHLCV                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_ohlcv(self, ohlcv):
        """ Cleans OHLCV fetched from an exchange """

        # NOTE: Sorting and date range trimming is already handled in the base class

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _VALIDATE OHLCV                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _validate_ohlcv(self, ohlcv):
        """
        Validates a list of OHLCV fetched and cleaned from an exchange
        """

        # Check if OHLCV is not a list
        if type(ohlcv) is not list:

            # Raise exception
            raise Exception("Cleaned OHLCV data should be returned as a list")

        # Check if any candles have an incorrect profile
        if any([len(o) != 6 for o in ohlcv]):

            # Raise exception
            raise Exception("Each candlestick should contain MS, O, H, L, C, V data")

        # Check if any candles have an incorrect type

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET OHLCV                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_ohlcv(
        self,
        symbol,
        timeframe,
        start,
        end=None,
        columns=None,
        use_mongo=False,
        with_times=False,
        as_dataframe=False,
    ):
        """
        Fetches, cleans, validates, and returns a list or dataframe of OHLCV from a data
        source in the following order of preference MongoDB (using ArcticDB) or the
        exchange itself (a lot slower due to rate and payload limiting)
        """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ TIMES                                                                      │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize start time
        _time_start = with_times and time.time()

        # Initialize times
        _times = (
            {
                EXCHANGE_READ: 0,
                MONGO_READ: 0,
                MONGO_WRITE: 0,
                TOTAL: 0,
            }
            if with_times
            else None
        )

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE AND VALIDATE INPUTS                                             │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Validate timeframe
        self.validate_timeframe(timeframe)

        # Initialize columns
        columns = columns and list(columns)

        # Initialize end datetime
        end = end or get_datetime_now_utc()

        # Iterate over start and end
        for dt, label in ((start, "Start"), (end, "End")):

            # Check if timezone is not UTC
            if not is_timezone_utc(dt):

                # Raise InvalidTimezoneError
                raise InvalidTimezoneError(f"{label} datetime must be in pytz.UTC")

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ START AND END                                                              │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get timeframe info
        timeframe_info = self.get_timeframe(timeframe)

        # Get frequency, chunk and gap
        frequency, chunk, gap = [timeframe_info[key] for key in (FREQUENCY, CHUNK, GAP)]

        # Floor start, e.g. 2021-05-25 06:00 --> 2021-05-25 00:00 @ 1m chunked by 1D
        start = self.floor_by_timeframe(start, timeframe)

        # Ceil end, e.g. 2021-05-26 13:00 --> 2021-05-26 23:59 @ 1m chunked by 1D
        # NOTE:          2021-06-01 00:00 --> 2021-06-01 00:00, i.e. already ceiling
        end = self.ceil_by_timeframe(end, timeframe)

        # Get timezone now
        # now = datetime.now(pytz.UTC)

        # Determine if start frequency period is over
        # is_start_over = now > start + pd.to_timedelta(frequency)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE DATA VARIABLES                                                  │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Define database key
        key = f"{symbol}.{timeframe}"

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE MONGO VARIABLES                                                 │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get Mongo URI
        mongo_uri = self.mongo_uri

        # Define use Mongo
        use_mongo = use_mongo and mongo_uri

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HELPER: READ OHLCV EXCHANGE                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        def read_ohlcv_exchange(start, end):
            """ Reads OHLCV data from an exchange """

            # Initialize start time
            _time_start = with_times and time.time()

            # Get exchange OHLCV
            ohlcv = self._get_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                start=start,
                end=end,
                as_dataframe=True,
            )

            # Check if with times
            if with_times:

                # Record time taken to fetch from exchange
                _times[EXCHANGE_READ] += time.time() - _time_start

            # Return exchange OHLCV
            return ohlcv

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HELPER: WRITE OHLCV MONGO                                                  │
        # └────────────────────────────────────────────────────────────────────────────┘

        def write_ohlcv_mongo(ohlcv, library):
            """ Writes OHLCV data to a Mongo library """

            # Return if library is null
            if not library:
                return

            # Rename timestamp to date for Arctic compatibility
            ohlcv.index.rename(DATE, inplace=True)

            # Initialize write start time
            _time_start = with_times and time.time()

            # Save to Arctic DB library
            # NOTE: This write will drop the datetime index tz info!
            library.update(key, ohlcv, upsert=True)

            # Check if with times
            if with_times:

                # Record time taken to fetch from exchange
                _times[MONGO_WRITE] += time.time() - _time_start

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ OHLCV AND MONGO LIBRARY                                                    │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize OHLCV to None
        ohlcv = None

        # Initialize Mongo library to None
        library = None

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ MONGO                                                                      │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if should use Mongo
        if use_mongo:

            # Get exchange slug
            exchange_slug = self.slug

            # Initialize store
            store = Arctic(mongo_uri)

            # Check if library doesn't exist
            if self.slug not in store.list_libraries():

                # Initialize library
                store.initialize_library(exchange_slug, lib_type=CHUNK_STORE)

            # Get library
            library = store[exchange_slug]

            # Get OHLCV from Mongo
            ohlcv = self._get_ohlcv_mongo(
                library=library,
                key=key,
                start=start,
                end=end,
                columns=columns,
                frequency=frequency,
                chunk=chunk,
                read_ohlcv_exchange=read_ohlcv_exchange,
                write_ohlcv_mongo=write_ohlcv_mongo,
                _times=_times,
            )

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ EXCHANGE                                                                   │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if OHLCV is still None
        if ohlcv is None:

            # Get OHLCV from exchange
            ohlcv = self._get_ohlcv_exchange()

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RECORD TIMES                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if with times
        if with_times:

            # Record total time
            _times[TOTAL] += time.time() - _time_start

            # Convert OHLCv to a tuple
            ohlcv = (ohlcv, _times)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN OHLCV                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return OHLCV
        return ohlcv

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _GET OHLCV MONGO                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _get_ohlcv_mongo(
        self,
        library,
        key,
        start,
        end,
        columns,
        frequency,
        chunk,
        read_ohlcv_exchange,
        write_ohlcv_mongo,
        _times,
    ):
        """ Fetches OHLCV using the supplied Mongo URI """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HANDLE NON-EXISTENT DATA                                                   │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return None if the data does not exist
        if key not in library.list_symbols():
            return None

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HELPER: READ OHLCV MONGO                                                   │
        # └────────────────────────────────────────────────────────────────────────────┘

        def read_ohlcv_mongo(start, end):
            """ Reads OHLCV data from a Mongo library """

            # Get date range
            date_range = DateRange(
                start.replace(tzinfo=None),
                end.replace(tzinfo=None) if end else None,
            )  # Unfortunately, tzinfo is scrubbed from Arctic on write

            # Initialize start time
            _time_start = _times and time.time()

            # Get Mongo OHLCV
            ohlcv = library.read(key, chunk_range=date_range, columns=columns)

            # Check if start time is defined
            if _time_start:

                # Record time taken to fetch from exchange
                _times[MONGO_READ] += time.time() - _time_start

            # Return Mongo OHLCV
            return ohlcv

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ READ MONGO DATA                                                            │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Read Mongo OHLCV
        ohlcv = read_ohlcv_mongo(start, end)

        # Return None if dataframe is empty
        if ohlcv.empty:
            return None

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ OHLCV INDEX                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if fetched dataframe timezone is not None
        if ohlcv.index.tzinfo is not None:

            # Raise InvalidTimezoneError
            raise InvalidTimezoneError("Mongo OHLCV should be timezone naive on fetch")

            # NOTE: ArcticDB stores OHLCV as timezone naive
            # It is important to ensure that what we save to Mongo is UTC

        # Localize the OHLCV index to UTC
        ohlcv.index = ohlcv.index.tz_localize("UTC")

        # Rename date to timestamp for compatibility
        ohlcv.index.rename(TIMESTAMP, inplace=True)

        # Get min and max index
        idx_min = ohlcv.index.min()
        idx_max = ohlcv.index.max()

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ DATA MISSING AT BEGINNING                                                  │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if start is less than min index
        if start < idx_min:

            # Get new chunk start and chunk end
            chunk_start, chunk_end = get_chunk_range(
                start=start, end=idx_min, frequency=frequency, chunk=chunk
            )

            # Get OHLCV using the exchange adapter
            exchange_ohlcv = read_ohlcv_exchange(start=chunk_start, end=chunk_end)

            # Check if start period is over
            # to avoid writing incomplete data
            if is_start_over:

                # Write exchange OHLCV to Mongo
                write_ohlcv_mongo(exchange_ohlcv=exchange_ohlcv, library=library)

            # Check if columns
            if columns:

                # Filter columns
                exchange_ohlcv = exchange_ohlcv[columns]

            # Merge Mongo OHLCV into exchange OHLCV
            ohlcv = exchange_ohlcv.combine_first(ohlcv)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ DATA MISSING AT END                                                        │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if end is greater than max index
        if end > idx_max:

            # Get new chunk start and chunk end
            chunk_start, chunk_end = get_chunk_range(start=idx_max, end=end)

            # Get OHLCV using the exchange adapter
            exchange_ohlcv = read_ohlcv_exchange(start=chunk_start, end=chunk_end)

            # Write exchange OHLCV to Mongo
            write_ohlcv_mongo(
                exchange_ohlcv=get_end_over_ohlcv(exchange_ohlcv),
                library=library,
            )

            # Check if columns
            if columns:

                # Filter columns
                exchange_ohlcv = exchange_ohlcv[columns]

            # Merge Mongo OHLCV into exchange OHLCV
            ohlcv = exchange_ohlcv.combine_first(ohlcv)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ DATA MISSING IN BETWEEN (GAPS)                                             │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Define gaps OHLCV as just the index of the current OHLCV
        gaps = mongo_ohlcv[[]].copy()

        # Add start column as index
        gaps[_c.START] = gaps.index

        # Define start as previous timestamp + 1 frequency
        gaps[_c.START] = gaps[_c.START].shift() + pd.Timedelta(frequency)

        # Define end as current timestamp - 1 frequency
        gaps[_c.END] = gaps.index - pd.Timedelta(frequency)

        # Define gap mask
        mask = gaps.index.to_series().diff() >= pd.Timedelta(gap_max)

        # Filter by mask
        gaps = gaps[mask]

        # Iterate over start and end for each gap
        for gap_start, gap_end in gaps.itertuples(index=False):

            # Get new chunk start and chunk end
            chunk_start, chunk_end = get_chunk_range(start=gap_start, end=gap_end)

            # Get OHLCV using the exchange adapter
            exchange_ohlcv = read_exchange_ohlcv(start=chunk_start, end=chunk_end)

            # Write exchange OHLCV to Mongo
            write_mongo_ohlcv(
                exchange_ohlcv=get_end_over_ohlcv(exchange_ohlcv),
                library=library,
            )

            # Check if columns
            if columns:

                # Filter columns
                exchange_ohlcv = exchange_ohlcv[columns]

            # Merge Mongo OHLCV into exchange OHLCV
            mongo_ohlcv = exchange_ohlcv.combine_first(mongo_ohlcv)

        # Slice Mongo OHLCV by start and end
        mongo_ohlcv = mongo_ohlcv.loc[start:end]

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN OHLCV                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return OHLCV
        return mongo_ohlcv

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET OHLCV                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __get_ohlcv(
        self,
        symbol,
        timeframe,
        start,
        end=None,
        columns=None,
        as_dataframe=False,
        use_mongo=False,
        with_times=False,
    ):
        """
        Fetches, cleans, validates, and returns a list or dataframe of OHLCV from a data
        source in the following order of preference MongoDB (using ArcticDB) or the
        exchange itself (a lot slower due to rate and payload limiting)
        """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HELPER: GET END OVER OHLCV                                                 │
        # └────────────────────────────────────────────────────────────────────────────┘

        def get_end_over_ohlcv(ohlcv):
            """ Subsets an OHLCV dataframe where index frequency period is over """

            # Get mask
            mask = now > ohlcv.index + pd.to_timedelta(frequency)

            # Return df subset
            return ohlcv[mask]

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ MONGO                                                                      │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if should use Mongo and Mongo URI is defined
        if use_mongo:
            pass

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ EXCHANGE                                                                   │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get chunk start and chunk end
        chunk_start, chunk_end = (
            get_chunk_range(start=start, end=end) if use_mongo else (start, end)
        )

        chunk_start, chunk_end = get_chunk_range(start=start, end=end)

        # Get OHLCV using the exchange adapter
        exchange_ohlcv = read_exchange_ohlcv(start=chunk_start, end=chunk_end)

        # Check if should write to Mongo
        if use_mongo and is_start_over:

            # Write exchange OHLCV to Mongo
            write_mongo_ohlcv(
                exchange_ohlcv=get_end_over_ohlcv(exchange_ohlcv), library=library
            )

        # Check if columns
        if columns:

            # Filter columns
            exchange_ohlcv = exchange_ohlcv[columns]

        # Slice exchange OHLCV by start and end
        exchange_ohlcv = exchange_ohlcv.loc[start:end]

        # Check if with times
        if with_times:

            # Record total time
            times[_c.TOTAL] += time.time() - get_ohlcv_start

            # Return OHLCV with times
            return (exchange_ohlcv, times)

        # Return OHLCV
        return exchange_ohlcv

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _GET OHLCV                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _get_ohlcv(self, symbol, timeframe, start, end=None, as_dataframe=False):
        """
        Fetches, cleans, validates, and returns a list or dataframe of OHLCV
        """

        # Initialize end
        end = end or datetime.now(pytz.UTC) + timedelta(seconds=30)

        # Fetch OHLCV
        ohlcv = self.fetch_ohlcv(
            symbol=symbol, timeframe=timeframe, start=start, end=end
        )

        # Clean OHLCV
        ohlcv = self.clean_ohlcv(ohlcv)

        # Validate OHLCV
        self._validate_ohlcv(ohlcv)

        # Trim by date range
        ohlcv = [c for c in ohlcv if start <= c[0] <= end]

        # Initialize seen timestamps
        seen_timestamps = set()

        # Remove duplicates by timestamp, keeping last occurance
        ohlcv = [
            c
            for c in ohlcv[::-1]
            if not (c[0] in seen_timestamps or seen_timestamps.add(c[0]))
        ]

        # Sort OHLCV by timestamp
        ohlcv = sorted(ohlcv, key=lambda x: x[0])

        # Check if OHLCV should be converted into a Pandas dataframe
        if as_dataframe:

            # Convert OHLCV to Pandas dataframe
            ohlcv = pd.DataFrame(
                ohlcv,
                columns=[_c.TIMESTAMP, _c.OPEN, _c.HIGH, _c.LOW, _c.CLOSE, _c.VOLUME],
            )

            # Set timestamp as index
            ohlcv.set_index(_c.TIMESTAMP, inplace=True)

            # Cast all columns as float32 (8 decimal places)
            # Decimal type is not supported by Pandas
            ohlcv = ohlcv.astype("float32")

        # Return OHLCV
        return ohlcv
