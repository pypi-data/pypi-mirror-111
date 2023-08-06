# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.exceptions import InvalidTimeframeError
from backwise.tools import get_timeframes


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

API = _c.API
CHUNK = _c.CHUNK
FREQUENCY = _c.FREQUENCY
GAP = _c.GAP
LABEL = _c.LABEL
TYPE = _c.TYPE


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE TIMEFRAME MIXIN                                                           │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ExchangeTimeframeMixin:
    """ A mixin class for dealing with exchange timeframes """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize timeframes cache to None
    _timeframes = None

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FETCH TIMEFRAMES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def fetch_timeframes(self):
        """ Fetches timeframes from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLEAN TIMEFRAMES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def clean_timeframes(self, timeframes):
        """ Cleans timeframes fetched from an exchange """

        raise NotImplementedError

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ TIMEFRAME INTERFACE                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define timeframe interface
    interface_timeframe = {
        LABEL: {TYPE: str},
        FREQUENCY: {TYPE: str},
        CHUNK: {TYPE: str},
        GAP: {TYPE: str},
        API: {TYPE: str},
    }

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _VALIDATE TIMEFRAMES                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _validate_timeframes(self, timeframes):
        """ Validates timeframes fetched and cleaned from an exchange """

        # Call validate method
        return self._validate_by_interface(
            "Timeframe", timeframes, self.interface_timeframe
        )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET TIMEFRAMES                                                                 │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_timeframes(self, timeframes=None):
        """ Fetches, cleans, validates, and returns timeframes from an exchange """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ GET CACHED TIMEFRAMES                                                      │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Rename timeframes to keys
        keys = timeframes

        # Get cached timeframes
        timeframes = self._timeframes

        # Check if timeframes is null
        if not timeframes:

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ FETCH AND CLEAN TIMEFRAMES                                             │
            # └────────────────────────────────────────────────────────────────────────┘

            # Fetch exchange timeframes
            timeframes_exchange = self.fetch_timeframes()

            # Clean exchange timeframes
            timeframes_exchange = self.clean_timeframes(timeframes_exchange)

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ MERGE TIMEFRAMES                                                       │
            # └────────────────────────────────────────────────────────────────────────┘

            # NOTE: Valid timeframes are the union between Backwise and the exchange

            # Initialize timeframes to empty dict
            timeframes = {}

            # Iterate over backwise timeframes
            for timeframe, info in get_timeframes().items():

                # Continue if timeframe not in exchange timeframes
                if timeframe not in timeframes_exchange:
                    continue

                # Add timeframe to timeframes
                timeframes[timeframe] = {k: v for k, v in info.items()}

                # Get exchange info
                info_exchange = timeframes_exchange[timeframe]

                # Check if exchange timeframe info is not a dict
                if type(info_exchange) is not dict:

                    # Treat value as the API timeframe
                    info_exchange = {API: info_exchange}

                # Update info by exchange timeframe
                timeframes[timeframe].update(info_exchange)

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ VALIDATE AND CACHE TIMEFRAMES                                          │
            # └────────────────────────────────────────────────────────────────────────┘

            # Validate timeframes
            self._validate_timeframes(timeframes)

            # Update cached timeframes
            self._timeframes = timeframes

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ FILTER KEYS                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if keys is defined
        if keys:

            # Filter timeframes
            timeframes = {
                timeframe: info
                for timeframe, info in timeframes.items()
                if timeframe in keys
            }

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN TIMEFRAMES                                                          │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return timeframes
        return timeframes

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET TIMEFRAME                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_timeframe(self, timeframe):
        """ Returns the timeframe associated with a given timeframe """

        # Get timeframes
        timeframes = self.get_timeframes(timeframes=[timeframe])

        # Return the timeframe
        return timeframes.get(timeframe, None)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ TIMEFRAME IS VALID                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def timeframe_is_valid(self, timeframe):
        """ Returns a boolean of whether or not the supplied timeframe is valid """

        # Return timeframe is valid boolean
        return timeframe in self.get_timeframes()

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ VALIDATE TIMEFRAME                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def validate_timeframe(self, timeframe):
        """ Validates a timeframe based on the exchange's available t}imeframes """

        # Check if timeframe is not valid
        if not self.timeframe_is_valid(timeframe):

            # Raise InvalidTimeframeError
            raise InvalidTimeframeError(
                f"Timeframe {timeframe} is invalid. Please use one of the following: "
                f"{', '.join(self.get_timeframes().keys())}"
            )
