from __future__ import division, unicode_literals

from decimal import Decimal, ROUND_HALF_UP
import warnings

import babel.core


class Amount(object):
    """An amount of particular currency.
    """
    __slots__ = ('value', 'currency')

    def __init__(self, value, currency):
        if isinstance(value, float):
            warnings.warn(  # pragma: no cover
                RuntimeWarning(
                    'float passed as value to Amount, consider using Decimal'),
                stacklevel=2)
        self.value = Decimal(value)
        self.currency = currency

    def __repr__(self):
        return 'Amount(%r, %r)' % (str(self.value), self.currency)

    def __lt__(self, other):
        if isinstance(other, Amount):
            if self.currency != other.currency:
                raise ValueError(
                    'Cannot compare amounts in %r and %r' % (
                        self.currency, other.currency))
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self == other:
            return True
        return self < other

    def __gt__(self, other):
        if isinstance(other, Amount):
            if self.currency != other.currency:
                raise ValueError(
                    'Cannot compare amounts in %r and %r' % (
                        self.currency, other.currency))
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if self == other:
            return True
        return self > other

    def __eq__(self, other):
        if isinstance(other, Amount):
            return (
                self.value == other.value and
                self.currency == other.currency)
        return False

    def __ne__(self, other):
        return not self == other

    def __mul__(self, other):
        try:
            value = self.value * other
        except TypeError:
            return NotImplemented
        return Amount(value=value, currency=self.currency)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Amount):
            if self.currency != other.currency:
                raise ValueError(
                    'Cannot divide amounts in %r and %r' % (
                        self.currency, other.currency))
            return self.value / other.value
        try:
            value = self.value / other
        except TypeError:
            return NotImplemented
        return Amount(value=value, currency=self.currency)

    def __div__(self, other):
        return self.__truediv__(other)

    def __add__(self, other):
        if isinstance(other, Amount):
            if other.currency != self.currency:
                raise ValueError(
                    'Cannot add amount in %r to %r' % (
                        self.currency, other.currency))
            value = self.value + other.value
            return Amount(value=value, currency=self.currency)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Amount):
            if other.currency != self.currency:
                raise ValueError(
                    'Cannot subtract amount in %r from %r' % (
                        other.currency, self.currency))
            value = self.value - other.value
            return Amount(value=value, currency=self.currency)
        return NotImplemented

    def __bool__(self):
        return bool(self.value)

    def __nonzero__(self):
        return self.__bool__()

    def quantize(self, exp=None, rounding=None):
        """Returns a quantized copy of the amount.

        If `exp` is given the resulting exponent will match that of `exp`.

        Otherwise the resulting exponent will be set to the correct exponent
        of the currency if it's known and to default (two decimal places)
        otherwise.
        """
        if rounding is None:
            rounding = ROUND_HALF_UP
        if exp is None:
            currencies = babel.core.get_global('currency_fractions')
            try:
                digits = currencies[self.currency][0]
            except KeyError:
                digits = currencies['DEFAULT'][0]
            exp = Decimal('0.1') ** digits
        else:
            exp = Decimal(exp)
        return Amount(
            value=self.value.quantize(exp, rounding=rounding),
            currency=self.currency)
