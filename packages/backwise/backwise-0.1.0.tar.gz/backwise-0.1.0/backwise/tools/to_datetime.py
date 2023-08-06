# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import pytz

from datetime import datetime

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from backwise.exceptions import InvalidInputError


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TO DATETIME                                                                        │
# └────────────────────────────────────────────────────────────────────────────────────┘


def to_datetime(value, timezone=None, unit_ms=False):
    """ Converts a value to a datetime object """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ VALUE TYPE                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Get value type
    value_type = type(value)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ TIMESTAMP                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Check if value is an integer or float
    if value_type in [int, float]:

        # Check if unit is milliseconds
        if unit_ms is True:

            # Divide value by 1000
            value /= 1000

        # Return a datetime object from a timestamp
        return datetime.fromtimestamp(value, tz=timezone)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ HANDLE INVALID INPUT                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Raise InvalidInputError
    raise InvalidInputError(
        f"Value {value} of type {value_type} cannot be converted to datetime"
    )


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TO DATETIME UTC                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘


def to_datetime_utc(value, unit_ms=False):
    """ Converts a value to a datetime with a UTC timezone """

    # Return datetime object
    return to_datetime(value, timezone=pytz.UTC, unit_ms=unit_ms)
