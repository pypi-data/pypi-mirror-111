# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import pytz

from datetime import datetime


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GET DATETIME NOW                                                                   │
# └────────────────────────────────────────────────────────────────────────────────────┘


def get_datetime_now(timezone=None):
    """ Returns a timezone-aware datetime object in UTC """

    # Return now datetime
    return datetime.now(tz=timezone)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GET DATETIME NOW UTC                                                               │
# └────────────────────────────────────────────────────────────────────────────────────┘


def get_datetime_now_utc():
    """ Returns a timezone-aware datetime object in UTC """

    # Return UTC now datetime
    return get_datetime_now(timezone=pytz.UTC)
