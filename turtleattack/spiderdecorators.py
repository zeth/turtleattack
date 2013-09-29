"""Code that makes the Spider class better.

These are decorators. Decorators are a more intermediate topic so have been
separated into this file.
"""

from functools import wraps


def reuse_doc(original_func):
    """Use the original docstring from the given parent class."""
    def original_doc(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        docstring = original_func.__doc__
        docstring = docstring.replace('turtle', 'spider')
        docstring = docstring.replace('Turtle', 'Spider')
        wrapper.__doc__ = docstring
        return wrapper
    return original_doc


def living_required(func):
    """If a spider is squished,
    it cannot move, at least not on earth."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].squished:
            print("Sadly, that spider is squished.")
        else:
            return func(*args, **kwargs)
    return wrapper


def individualise_lines(func):
    """Make breaks in lines so that turtles break smaller sections of web."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        instance.penup()
        instance.pendown()
        output = func(*args, **kwargs)
        instance.penup()
        instance.pendown()
        return output
    return wrapper
