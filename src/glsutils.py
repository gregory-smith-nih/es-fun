"""
gregs utilities
"""


def get(obj, path, default):
    """
    get the dictionary value, if anything goes wrong, return the default.
    path = "key.key.key..."
    """
    result = obj
    try:
        for key in path.split("."):
            result = result[key]
    except:
        result = default
    return result
