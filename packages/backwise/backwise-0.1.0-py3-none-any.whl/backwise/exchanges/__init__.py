# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import ccxt

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from backwise.exceptions import UnsupportedExchangeError
from backwise.exchanges._ccxt import CCXTExchange
from backwise.exchanges.binance import Binance
from backwise.tools import to_slug


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GET EXCHANGE CLASS                                                                 │
# └────────────────────────────────────────────────────────────────────────────────────┘


def get_exchange_class(slug):
    """ Returns an uninitialized Backwise based on a slug """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ EXCHANGE CLASSES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define exchange classes
    exchange_classes = {exchange.get_slug(): exchange for exchange in (Binance,)}

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ BACKWISE-DEFINED EXCHANGES                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Ensure slug is really a slug
    slug = to_slug(slug)

    # Check if slug in exchange classes
    if slug in exchange_classes:

        # Return Backwise exchange class
        return exchange_classes[slug]

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ DYNAMIC CCXT EXCHANGE                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Get CCXT exchange
    ccxt_exchange = getattr(ccxt, slug, None)

    # Check if CCXT exchange is not None
    if ccxt_exchange is not None:

        # Initialize CCXT exchange
        ccxt_exchange = ccxt_exchange()

        # Get CCXT exchange name
        ccxt_exchange_name = ccxt_exchange.name

        # Create a new class that inherits from CCXTExchange
        class DynamicCCXTExchange(CCXTExchange):
            """ A dynamically-defined Backwise CCXT exchange """

            # Define name
            name = ccxt_exchange_name

        # Return DynamicCCXTExchange
        return DynamicCCXTExchange

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ UNSUPPORTED EXCHANGE                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Raise UnsupportedExchangeError
    raise UnsupportedExchangeError(f"An exchange class for {slug} could not be found.")
