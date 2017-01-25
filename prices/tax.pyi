from decimal import Decimal

from typing import Union

from .amount import Amount
from .price import Price


Numeric = Union[int, Decimal]


class Tax:
    name = ...  # type: str

    def apply(self, other): ...

    def calculate_tax(self, price: Price) -> Amount: ...


class LinearTax(Tax):
    def __init__(self, multiplier: Numeric, name: str=None) -> None: ...

    def __repr__(self) -> str: ...

    def __lt__(self, other: LinearTax) -> bool: ...

    def __gt__(self, other: LinearTax) -> bool: ...

    def __eq__(self, other: object) -> bool: ...

    def __ne__(self, other: object) -> bool: ...

    def calculate_tax(self, price: Price) -> Amount: ...
