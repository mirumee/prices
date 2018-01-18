from decimal import Decimal
from typing import Optional, Union, overload

from .money import Money
from .taxed_money import TaxedMoney
from .taxed_money_range import TaxedMoneyRange

Numeric = Union[int, Decimal]


class Tax:
    """A generic tax class, provided so all taxers have a common base."""

    @overload
    def apply(self, other: TaxedMoney) -> TaxedMoney:
        ...  # pragma: no cover

    @overload
    def apply(self, other: TaxedMoneyRange) -> TaxedMoneyRange:
        ...  # pragma: no cover

    def apply(self, other):
        if isinstance(other, TaxedMoney):
            return TaxedMoney(
                net=other.net,
                gross=other.gross + self.calculate(other))
        elif isinstance(other, TaxedMoneyRange):
            return TaxedMoneyRange(
                self.apply(other.start), self.apply(other.stop))
        else:
            raise TypeError('Cannot apply tax to %r' % (other,))

    def calculate(self, base: TaxedMoney) -> Money:
        """Calculate the tax amount."""
        raise NotImplementedError()


class LinearTax(Tax):
    """Adds a certain fraction on top of the price."""

    def __init__(self, multiplier: Numeric, name=None) -> None:
        self.multiplier = Decimal(multiplier)
        self.name = name

    def __repr__(self) -> str:
        return 'LinearTax(%r, name=%r)' % (str(self.multiplier), self.name)

    def __lt__(self, other: 'LinearTax') -> bool:
        if isinstance(other, LinearTax):
            return self.multiplier < other.multiplier
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LinearTax):
            return (
                self.multiplier == other.multiplier and
                self.name == other.name)
        return False

    def __le__(self, other: 'LinearTax') -> bool:
        if self == other:
            return True
        return self < other

    def calculate(self, base: TaxedMoney) -> Money:
        return base.net * self.multiplier
