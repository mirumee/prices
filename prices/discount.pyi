import decimal

from typing import overload

from .amount import Amount, Numeric
from .price import Price
from .price_range import PriceRange


class Discount:
    name = ...  # type: str

    @overload
    def apply(self, other: Price) -> Price: ...
    @overload
    def apply(self, other: PriceRange) -> PriceRange: ...

    def calculate_price(self, price: Price) -> Price: ...


class FixedDiscount(Discount):
    amount = ...  # type: Amount

    def __init__(self, amount: Amount, name: str=None) -> None: ...

    def __repr__(self) -> str: ...

    def calculate_price(self, price: Price) -> Price: ...


class FractionalDiscount(Discount):
    factor = ...  # Decimal

    def __init__(self, factor: Numeric, name: str=None) -> None: ...

    def __repr__(self) -> str: ...

    def calculate_price(self, price: Price) -> Price: ...


def percentage_discount(value: Numeric, name: str=None) -> FractionalDiscount: ...
