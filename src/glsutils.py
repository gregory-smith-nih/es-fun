"""
gregs utilities
"""
import json
import sys

def isArray(obj):
    return isinstance(obj, list)

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

def set(obj, path, value):
    """
    set the dictionary value, if anything goes wrong, return the default.
    path = "key.key.key..."
    """
    newobj = obj
    keys = path.split(".")
    for key in keys[:-1]:
        try:
            newobj = newobj[key]
        except:
            newobj[key] = {}
            newobj = newobj[key]
    newobj[keys[-1]] = value

def error(s):
    print(s, file=sys.stderr)

def jdumps(obj):
    return json.dumps(obj, indent=4, separators=(",", ": "), sort_keys=True)

def jprint(obj):
    print(jdumps(obj))


def jerror(obj):
    error(jdumps(obj))
