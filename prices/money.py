import warnings
from decimal import ROUND_HALF_UP, Decimal
from typing import overload

from babel.numbers import get_currency_precision

Numeric = int | Decimal


class Money:
    """An amount of a particular currency."""

    __slots__ = ("amount", "currency")

    def __init__(self, amount: Numeric, currency: str) -> None:
        if isinstance(amount, float):
            warnings.warn(  # pragma: no cover
                RuntimeWarning(
                    "float passed as value to Money, consider using Decimal"
                ),
                stacklevel=2,
            )
        self.amount = Decimal(amount)
        self.currency = currency

    def __repr__(self) -> str:
        return f"Money({str(self.amount)!r}, {self.currency!r})"

    def __lt__(self, other: "Money") -> bool:
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(
                    f"Cannot compare amounts in {self.currency!r} "
                    f"and {other.currency!r}"
                )
            return self.amount < other.amount
        return NotImplemented

    def __le__(self, other: "Money") -> bool:
        if self == other:
            return True
        return self < other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Money):
            return self.amount == other.amount and self.currency == other.currency
        return False

    def __mul__(self, other: Numeric) -> "Money":
        try:
            amount = self.amount * other
        except TypeError:
            return NotImplemented
        return Money(amount, self.currency)

    def __rmul__(self, other: Numeric) -> "Money":
        return self * other

    @overload
    def __truediv__(self, other: "Money") -> Decimal: ...  # pragma: no cover

    @overload
    def __truediv__(self, other: Numeric) -> "Money": ...  # pragma: no cover

    def __truediv__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(
                    f"Cannot divide amounts in {self.currency!r} "
                    f"and {other.currency!r}"
                )
            return self.amount / other.amount
        try:
            amount = self.amount / other
        except TypeError:
            return NotImplemented
        return Money(amount, self.currency)

    def __add__(self, other: "Money") -> "Money":
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise ValueError(
                    f"Cannot add amount in {self.currency!r} to {other.currency!r}"
                )
            amount = self.amount + other.amount
            return Money(amount, self.currency)
        return NotImplemented

    def __sub__(self, other: "Money") -> "Money":
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise ValueError(
                    f"Cannot subtract amount in {other.currency!r} "
                    f"from {self.currency!r}"
                )
            amount = self.amount - other.amount
            return Money(amount, self.currency)
        return NotImplemented

    def __bool__(self) -> bool:
        return bool(self.amount)

    def quantize(self, exp=None, rounding=None) -> "Money":
        """Return a copy of the object with its amount quantized.

        If `exp` is given the resulting exponent will match that of `exp`.

        Otherwise the resulting exponent will be set to the correct exponent
        of the currency if it's known and to default (two decimal places)
        otherwise.
        """
        if rounding is None:
            rounding = ROUND_HALF_UP
        if exp is None:
            digits = get_currency_precision(self.currency)
            exp = Decimal("0.1") ** digits
        else:
            exp = Decimal(exp)
        return Money(self.amount.quantize(exp, rounding=rounding), self.currency)
