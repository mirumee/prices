import functools
import operator


def sum(values):
    """Returns a sum of given values.
    """
    return functools.reduce(operator.add, values)
