# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import pandas as pd
import pytz

from datetime import timedelta
from decimal import Decimal

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.mixins import (
    ExchangeAmountMixin,
    ExchangeCurrencyMixin,
    ExchangeInterfaceMixin,
    ExchangeMarketMixin,
    ExchangeOHLCVMixin,
    ExchangeTickerMixin,
    ExchangeTimeframeMixin,
    ExchangeTradeMixin,
)
from backwise.tools import to_slug


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE                                                                           │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Exchange(
    ExchangeInterfaceMixin,
    ExchangeTimeframeMixin,
    ExchangeMarketMixin,
    ExchangeCurrencyMixin,
    ExchangeTickerMixin,
    ExchangeOHLCVMixin,
    ExchangeAmountMixin,
    ExchangeTradeMixin,
):
    """ A base class for Backwise exchanges """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ TODO                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # TODO: Implement symbol validation, like with timeframe

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize exchange name and slug
    name = slug = ""

    # Initialize timeout to 30 seconds
    # NOTE: Timeout used for API calls
    timeout_ms = 30000

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ GET SLUG                                                                       │
    # └────────────────────────────────────────────────────────────────────────────────┘

    @classmethod
    def get_slug(cls):
        """ Returns a slug based on the exchange name """

        return to_slug(cls.name, space="_")

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ INIT METHOD                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __init__(
        self,
        *args,
        api_key_read="",
        api_secret_read="",
        api_key_trade="",
        api_secret_trade="",
        mongo_uri="",
        **kwargs,
    ):
        """ Init Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ INITIALIZE PARENT                                                          │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Call parent init method
        super().__init__(*args, **kwargs)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ NAME AND SLUG                                                              │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Assert that exchange name is defined
        assert self.name, "Class attribute for exchange name cannot be null"

        # Get exchange slug
        self.slug = self.get_slug()

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ CREDENTIALS                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Set credentials
        self.api_key_read = api_key_read
        self.api_secret_read = api_secret_read
        self.api_key_trade = api_key_trade
        self.api_secret_trade = api_secret_trade

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ MONGO                                                                      │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Set Mongo URI
        self.mongo_uri = mongo_uri

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ CACHES                                                                     │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize cached trading fees
        self._trading_fees = {}
