# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from decimal import Decimal

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import backwise.constants as _c

from backwise.exceptions import InterfaceError


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CONSTANTS                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘

NULL = _c.NULL
TYPE = _c.TYPE
VALIDATOR = _c.VALIDATOR


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EXCHANGE INTERFACE MIXIN                                                           │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ExchangeInterfaceMixin:
    """ A mixin class for handling exchange interfaces """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _VALIDATE BY INTERFACE                                                         │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _validate_by_interface(self, label, items, interface):
        """ Validates a set of items based on an interface """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ TYPE DEFINITIONS                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize value types
        value_types = {}

        # Iterate over interface
        for key, info in interface.items():

            # Get value type
            value_type = info[TYPE]
            value_type = value_type if type(value_type) is list else [value_type]

            # Ensure None is handled correctly
            value_type = [type(t) if t is None else t for t in value_type]

            # Add value type to value types
            value_types[key] = value_type

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ ITERATE OVER ITEMS                                                         │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Iterate over items
        for item in items.values() if type(items) is dict else items:

            # ┌────────────────────────────────────────────────────────────────────────┐
            # │ ITERATE OVER INTERFACE                                                 │
            # └────────────────────────────────────────────────────────────────────────┘

            # Iterate over item interface
            for key, info in interface.items():

                # Get expected types
                expected_types = value_types[key]

                # ┌────────────────────────────────────────────────────────────────────┐
                # │ HANDLE MISSING                                                     │
                # └────────────────────────────────────────────────────────────────────┘

                # Check if key not in item
                if key not in item:

                    # Raise exception
                    raise InterfaceError(
                        f"{label} missing {key} of type {expected_types}"
                    )

                # ┌────────────────────────────────────────────────────────────────────┐
                # │ HANDLE TYPE                                                        │
                # └────────────────────────────────────────────────────────────────────┘

                # Get value and type
                value = item[key]
                value_type = type(value)

                # Check if value is missing or not the correct type
                if type(value) not in expected_types:

                    # Raise exception
                    raise InterfaceError(
                        f"{label} {key} is not of type {expected_types}"
                    )

                # ┌────────────────────────────────────────────────────────────────────┐
                # │ HANDLE NULL                                                        │
                # └────────────────────────────────────────────────────────────────────┘

                # Get value null
                value_null = info.get(NULL, False)

                # Check if value is null and cannot be null
                if not value_null and not value:

                    # Check if value type is non-numerical
                    if value_type not in (bool, int, float, Decimal):

                        # Raise exception
                        raise InterfaceError(
                            f"{label} value for {key} cannot be nullish"
                        )

                # ┌────────────────────────────────────────────────────────────────────┐
                # │ HANDLE VALIDATOR                                                   │
                # └────────────────────────────────────────────────────────────────────┘

                # Get value validator
                value_validator = info.get(VALIDATOR)

                # Check if custom validator is defined
                if value_validator and not value_validator(value):

                    # Raise exception
                    raise InterfaceError(f"{label} {key} is not valid: {value}")

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ RETURN ITEMS                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Return items
        return items
