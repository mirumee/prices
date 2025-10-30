from typing import TypeAlias

from prices.money import Money
from prices.money_range import MoneyRange
from prices.taxed_money import TaxedMoney

Addable: TypeAlias = "Money | MoneyRange | TaxedMoney | TaxedMoneyRange"


class TaxedMoneyRange:
    """A taxed money range."""

    __slots__ = ("start", "stop")

    def __init__(self, start: TaxedMoney, stop: TaxedMoney) -> None:
        if start.currency != stop.currency:
            raise ValueError(
                f"Cannot create a range as {start!r} and "
                f"{stop!r} use different currencies"
            )
        if start > stop:
            raise ValueError(f"Cannot create a range from {start!r} to {stop!r}")
        self.start = start
        self.stop = stop

    def __repr__(self) -> str:
        return f"TaxedMoneyRange({self.start!r}, {self.stop!r})"

    def __add__(self, other: Addable) -> "TaxedMoneyRange":
        if isinstance(other, (Money, TaxedMoney)):
            if other.currency != self.currency:
                raise ValueError(
                    f"Cannot add a range in {self.currency!r} "
                    f"to argument in {other.currency!r}"
                )
            start = self.start + other
            stop = self.stop + other
            return TaxedMoneyRange(start, stop)
        elif isinstance(other, (MoneyRange, TaxedMoneyRange)):
            if other.start.currency != self.currency:
                raise ValueError(
                    f"Cannot add ranges in {self.currency!r} and {other.currency!r}"
                )
            start = self.start + other.start
            stop = self.stop + other.stop
            return TaxedMoneyRange(start, stop)
        return NotImplemented

    def __sub__(self, other: Addable) -> "TaxedMoneyRange":
        if isinstance(other, (Money, TaxedMoney)):
            if other.currency != self.start.currency:
                raise ValueError(
                    f"Cannot subtract argument in {other.currency!r} "
                    f"from range in {self.start.currency!r}"
                )
            start = self.start - other
            stop = self.stop - other
            return TaxedMoneyRange(start, stop)
        elif isinstance(other, (MoneyRange, TaxedMoneyRange)):
            if other.start.currency != self.start.currency:
                raise ValueError(
                    f"Cannot subtract range in {other.start.currency!r} "
                    f"from {self.start.currency!r}"
                )
            start = self.start - other.start
            stop = self.stop - other.stop
            return TaxedMoneyRange(start, stop)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TaxedMoneyRange):
            return self.start == other.start and self.stop == other.stop
        return False

    def __contains__(self, item: TaxedMoney) -> bool:
        if not isinstance(item, TaxedMoney):
            raise TypeError(
                "`in taxed_money_range` requires TaxedMoney "
                f"as left operand, not {type(item)}"
            )
        return self.start <= item <= self.stop

    @property
    def currency(self) -> str:
        """Return the currency of the range."""
        return self.start.currency

    def quantize(self, exp=None, rounding=None) -> "TaxedMoneyRange":
        """Return a copy of the range with start and stop quantized.

        All arguments are passed to `TaxedMoney.quantize` which in turn calls
        `Money.quantize`.
        """
        return TaxedMoneyRange(
            self.start.quantize(exp, rounding=rounding),
            self.stop.quantize(exp, rounding=rounding),
        )

    def replace(
        self, start: TaxedMoney | None = None, stop: TaxedMoney | None = None
    ) -> "TaxedMoneyRange":
        """Return a range with start or stop replaced with given values."""
        if start is None:
            start = self.start
        if stop is None:
            stop = self.stop
        return TaxedMoneyRange(start=start, stop=stop)
