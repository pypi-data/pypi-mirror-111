class ExchangeMixin:
    """"""


## ┌────────────────────────────────────────────────────────────────────────────────────┐
## │ PROJECT IMPORTS                                                                    │
## └────────────────────────────────────────────────────────────────────────────────────┘
#
# from hodlsworth.exchange import get_exchange_class
#
#
## ┌────────────────────────────────────────────────────────────────────────────────────┐
## │ EXCHANGE MIXIN                                                                     │
## └────────────────────────────────────────────────────────────────────────────────────┘
#
#
# class ExchangeMixin:
#    """ A mixin class for caching Exchange objects """
#
#    # ┌────────────────────────────────────────────────────────────────────────────────┐
#    # │ EXCHANGE ADAPTERS                                                              │
#    # └────────────────────────────────────────────────────────────────────────────────┘
#
#    # Initialize exchanges
#    _exchanges = None
#
#    # ┌────────────────────────────────────────────────────────────────────────────────┐
#    # │ INIT METHOD                                                                    │
#    # └────────────────────────────────────────────────────────────────────────────────┘
#
#    def __init__(self, *args, mongo_uri="", **kwargs):
#        """ Init Method """
#
#        # Call parent init method
#        super().__init__(*args, **kwargs)
#
#        # Set Mongo URI
#        self.mongo_uri = mongo_uri
#
#        # Initialize exchanges
#        self._exchanges = {}
#
#    # ┌────────────────────────────────────────────────────────────────────────────────┐
#    # │ GET EXCHANGE                                                                   │
#    # └────────────────────────────────────────────────────────────────────────────────┘
#
#    def get_exchange(self, exchange_slug):
#        """ Returns an initialized instance of an exchange """
#
#        # ┌────────────────────────────────────────────────────────────────────────────┐
#        # │ INITIALIZE CACHE                                                           │
#        # └────────────────────────────────────────────────────────────────────────────┘
#
#        # Check if exchanges is None
#        if self._exchanges is None:
#
#            # Set exchanges to empty dict
#            self._exchanges = {}
#
#        # ┌────────────────────────────────────────────────────────────────────────────┐
#        # │ RETURN CACHED                                                              │
#        # └────────────────────────────────────────────────────────────────────────────┘
#
#        # Check if exchange slug in exchanges
#        if exchange_slug in self._exchanges:
#
#            # Return cached exchange
#            return self._exchanges[exchange_slug]
#
#        # ┌────────────────────────────────────────────────────────────────────────────┐
#        # │ INITIALIZE AND CACHE EXCHANGE                                              │
#        # └────────────────────────────────────────────────────────────────────────────┘
#
#        # Get exchange class
#        exchange = get_exchange_class(exchange_slug)
#
#        # Check if exchange is not null
#        if exchange:
#
#            # Initialize exchange
#            exchange = exchange(mongo_uri=self.mongo_uri)
#
#            # Cache exchange
#            self._exchanges[exchange_slug] = exchange
#
#        # Return exchange
#        return exchange
#
#    # ┌────────────────────────────────────────────────────────────────────────────────┐
#    # │ SET EXCHANGE                                                                   │
#    # └────────────────────────────────────────────────────────────────────────────────┘
#
#    def set_exchange(self, exchange):
#        """ Adds an initialized exchange to exchanges cache """
#
#        # ┌────────────────────────────────────────────────────────────────────────────┐
#        # │ INITIALIZE CACHE                                                           │
#        # └────────────────────────────────────────────────────────────────────────────┘
#
#        # Check if exchanges is None
#        if self._exchanges is None:
#
#            # Set exchanges to empty dict
#            self._exchanges = {}
#
#        # ┌────────────────────────────────────────────────────────────────────────────┐
#        # │ CACHE EXCHANGE                                                             │
#        # └────────────────────────────────────────────────────────────────────────────┘
#
#        # Add exchange to exchanges cache
#        self._exchanges[exchange.exchange_slug] = exchange
