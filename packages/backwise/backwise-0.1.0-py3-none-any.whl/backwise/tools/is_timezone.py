# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import pytz


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ IS TIMEZONE AWARE                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘


def is_timezone_aware(datetime, timezone=None):
    """ Determined if a datetime object is timezone aware """

    # Return a boolean of whether datetime is timezone aware
    return (
        datetime.tzinfo is not None
        and datetime.tzinfo.utcoffset(datetime) is not None
        and (timezone is None or datetime.tzinfo == timezone)
    )


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ IS TIMEZONE UTC                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘


def is_timezone_utc(datetime):
    """ Determined if a datetime object is timezone UTC """

    # Return a boolean of whether datetime is timezone UTC
    return is_timezone_aware(datetime, timezone=pytz.UTC)
