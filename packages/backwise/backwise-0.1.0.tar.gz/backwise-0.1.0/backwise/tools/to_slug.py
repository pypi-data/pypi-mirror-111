# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from unidecode import unidecode


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TO SLUG                                                                            │
# └────────────────────────────────────────────────────────────────────────────────────┘


def to_slug(string, decode=True, space=None):
    """ Returns a slugified version of a string input """

    # Return empty string if no text value passed
    if not string:
        return ""

    # Remove special characters
    if decode:
        string = unidecode(string)

    # Lowercase and strip slug
    string = string.lower().strip()

    # Check if space is a string
    if type(space) is str:

        # Replace spaces with the specified character
        string = string.replace(" ", space)

    # Return slugified string
    return string
