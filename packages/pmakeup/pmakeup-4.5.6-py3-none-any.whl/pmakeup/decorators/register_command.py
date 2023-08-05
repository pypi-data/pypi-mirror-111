import logging
from functools import wraps


def add(group: str = "generic"):
    def decorator(func):
        @wraps(func)
        def decorator_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        logging.debug("adding function \"{name}\"")
        function_name = func.__name__
        if function_name not in add.plugins["call_dictionary"]:
            add.plugins["call_dictionary"][function_name] = {}
        add.plugins["call_dictionary"][function_name] = (group, func)

        decorator.__doc__ = func.__doc__

        return decorator_wrapper

    if not hasattr(add, "plugins"):
        add.plugins = dict()
        add.plugins["call_dictionary"] = {}

    return decorator
