from decimal import Decimal
from typing import Optional, Union, overload

from .money import Money
from .taxed_money import TaxedMoney
from .taxed_money_range import TaxedMoneyRange

Numeric = Union[int, Decimal]


class Discount:
    """Base discount class."""

    name: Optional[str] = None

    @overload
    def apply(self, other: TaxedMoney) -> TaxedMoney:
        ...  # pragma: no cover

    @overload
    def apply(self, other: TaxedMoneyRange) -> TaxedMoneyRange:
        ...  # pragma: no cover

    def apply(self, other):
        """Apply the discount to a price or price range.

        Return a new discounted instance.
        """
        if isinstance(other, TaxedMoney):
            return self.calculate(other)
        elif isinstance(other, TaxedMoneyRange):
            return TaxedMoneyRange(
                self.apply(other.start), self.apply(other.stop))
        else:
            raise TypeError('Cannot apply discount to %r' % (other,))

    def calculate(self, base: TaxedMoney) -> TaxedMoney:
        """Calculate the price after discount."""
        raise NotImplementedError()


class FixedDiscount(Discount):
    """Reduces price by a fixed amount."""

    def __init__(self, amount: Money, name: str = None) -> None:
        self.amount = amount
        self.name = name or self.name

    def __repr__(self) -> str:
        return 'FixedDiscount(%r, name=%r)' % (self.amount, self.name)

    def calculate(self, base: TaxedMoney) -> TaxedMoney:
        if base.currency != self.amount.currency:
            raise ValueError(
                'Cannot apply a discount in %r to a base in %r' % (
                    self.amount.currency, base.currency))
        net = max(
            base.net - self.amount, Money(0, self.amount.currency))
        gross = max(
            base.gross - self.amount, Money(0, self.amount.currency))
        return TaxedMoney(net=net, gross=gross)


class FractionalDiscount(Discount):
    """Reduces price by a given fraction."""

    def __init__(self, factor: Decimal, name: str = None) -> None:
        self.factor = Decimal(factor)
        self.name = name or self.name

    def __repr__(self) -> str:
        return 'FractionalDiscount(%r, name=%r)' % (self.factor, self.name)

    def calculate(self, base: TaxedMoney) -> TaxedMoney:
        net_discount = base.net * self.factor
        gross_discount = base.gross * self.factor
        return TaxedMoney(
            net=(base.net - net_discount).quantize(),
            gross=(base.gross - gross_discount).quantize())


def percentage_discount(value: Numeric, name: str = None) -> FractionalDiscount:
    """Return a fractional discount given a percentage."""
    factor = Decimal(value) / 100
    return FractionalDiscount(factor, name)
