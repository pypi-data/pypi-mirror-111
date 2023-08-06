# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

PRECISION = _c.PRECISION
PRECISION_DISPLAY = _c.PRECISION_DISPLAY


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE AMOUNT MIXIN                                                              │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ExchangeAmountMixin:
    """ A mixin class for handling amount-related features of an exchange """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ ROUND AMOUNT                                                                   │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def round_amount(
        self, amount, currency_code, precision=None, display=False, symbols=None
    ):
        """ Rounds an amount based on its specific market precision """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HANDLE NONE AMOUNT                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return amount if amount is None
        if amount is None:
            return amount

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ HANDLE NONE PRECISION                                                      │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if precision is None
        if precision is None:

            # Get currency
            currency = self.get_currencies(symbols=symbols if display else None).get(
                currency_code
            )  # Symbols are really only relevant if rounding for a display

            # Check if currency
            if currency:

                # Get precision key
                precision_key = PRECISION_DISPLAY if display else PRECISION

                # Get precision
                precision = currency[precision_key]

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ ROUND AMOUNT                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Round amount
        amount = round(amount, precision) if precision is not None else amount

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN AMOUNT                                                              │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return amount
        return amount
