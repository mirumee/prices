import functools
import operator
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def sum(values: Iterable[T]) -> T:
    """Return a sum of given values."""
    return functools.reduce(operator.add, values)
