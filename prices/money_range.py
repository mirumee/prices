from prices.taxed_money import Money

Addable = "Money | MoneyRange"


class MoneyRange:
    """A taxed money range."""

    __slots__ = ("start", "stop")

    def __init__(self, start: Money, stop: Money) -> None:
        if start.currency != stop.currency:
            raise ValueError(
                f"Cannot create a range as {start!r} "
                f"and {stop!r} use different currencies"
            )
        if start > stop:
            raise ValueError(f"Cannot create a range from {start!r} to {stop!r}")
        self.start = start
        self.stop = stop

    def __repr__(self) -> str:
        return f"MoneyRange({self.start!r}, {self.stop!r})"

    def __add__(self, other: Addable) -> "MoneyRange":
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise ValueError(
                    f"Cannot add range in {self.currency!r} "
                    f"to argument in {other.currency!r}"
                )
            start = self.start + other
            stop = self.stop + other
            return MoneyRange(start, stop)
        elif isinstance(other, MoneyRange):
            if other.start.currency != self.currency:
                raise ValueError(
                    f"Cannot add ranges in {self.currency!r} and {other.currency!r}"
                )
            start = self.start + other.start
            stop = self.stop + other.stop
            return MoneyRange(start, stop)
        return NotImplemented

    def __sub__(self, other: Addable) -> "MoneyRange":
        if isinstance(other, Money):
            if other.currency != self.start.currency:
                raise ValueError(
                    f"Cannot subtract Money in {other.currency!r} "
                    f"from a range in {self.start.currency!r}"
                )
            start = self.start - other
            stop = self.stop - other
            return MoneyRange(start, stop)
        elif isinstance(other, MoneyRange):
            if other.start.currency != self.start.currency:
                raise ValueError(
                    f"Cannot subtract range in {other.start.currency!r} "
                    f"from {self.start.currency!r}"
                )
            start = self.start - other.start
            stop = self.stop - other.stop
            return MoneyRange(start, stop)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MoneyRange):
            return self.start == other.start and self.stop == other.stop
        return False

    def __contains__(self, item: Money) -> bool:
        if not isinstance(item, Money):
            raise TypeError(
                f"`in money_range` requires Money as left operand, not {type(item)}"
            )
        return self.start <= item <= self.stop

    @property
    def currency(self) -> str:
        """Return the currency of the range."""
        return self.start.currency

    def quantize(self, exp=None, rounding=None) -> "MoneyRange":
        """Return a copy of the range with start and stop quantized.

        All arguments are passed to `Money.quantize`.
        """
        return MoneyRange(
            self.start.quantize(exp, rounding=rounding),
            self.stop.quantize(exp, rounding=rounding),
        )

    def replace(self, start: Money = None, stop: Money = None) -> "MoneyRange":
        """Return a range with start or stop replaced with given values."""
        if start is None:
            start = self.start
        if stop is None:
            stop = self.stop
        return MoneyRange(start=start, stop=stop)
