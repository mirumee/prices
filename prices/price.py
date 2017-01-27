from __future__ import division, unicode_literals

import warnings

from .amount import Amount


class Price(object):
    """A price, provides amounts for net, gross (incl. tax) and tax.
    """
    __slots__ = ('net', 'gross')

    def __init__(self, net, gross):
        if not isinstance(net, Amount) or not isinstance(gross, Amount):
            raise TypeError('Price requires two amounts, got %r, %r' % (
                net, gross))
        self.net = net
        self.gross = gross

    def __repr__(self):
        return 'Price(net=%r, gross=%r)' % (self.net, self.gross)

    def __lt__(self, other):
        if isinstance(other, Price):
            return self.gross < other.gross
        elif isinstance(other, Amount):
            raise TypeError('Cannot compare prices and amounts')
        return NotImplemented

    def __le__(self, other):
        if self == other:
            return True
        return self < other

    def __gt__(self, other):
        if isinstance(other, Price):
            return self.gross > other.gross
        elif isinstance(other, Amount):
            raise TypeError('Cannot compare prices and amounts')
        return NotImplemented

    def __ge__(self, other):
        if self == other:
            return True
        return self > other

    def __eq__(self, other):
        if isinstance(other, Price):
            return (
                self.gross == other.gross and
                self.net == other.net)
        return False

    def __ne__(self, other):
        return not self == other

    def __mul__(self, other):
        try:
            price_net = self.net * other
            price_gross = self.gross * other
        except TypeError:
            return NotImplemented
        return Price(net=price_net, gross=price_gross)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        try:
            price_net = self.net / other
            price_gross = self.gross / other
        except TypeError:
            return NotImplemented
        return Price(net=price_net, gross=price_gross)

    def __div__(self, other):
        return self.__truediv__(other)

    def __add__(self, other):
        if isinstance(other, Price):
            price_net = self.net + other.net
            price_gross = self.gross + other.gross
            return Price(net=price_net, gross=price_gross)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Price):
            price_net = self.net - other.net
            price_gross = self.gross - other.gross
            return Price(net=price_net, gross=price_gross)
        return NotImplemented

    def __bool__(self):  # pragma: no cover
        warnings.warn(
            RuntimeWarning(
                '`bool(price)` will always evaluate to True, consider replacing the test with explicit `if price is None` or `if price.gross`.'),
            stacklevel=2)
        return True

    def __nonzero__(self):
        return self.__bool__()

    @property
    def currency(self):
        """Returns the currency of the price.
        """
        return self.net.currency

    @property
    def tax(self):
        """Returns the tax amount.
        """
        return self.gross - self.net

    def quantize(self, exp=None, rounding=None):
        """Returns a quantized copy of the price.

        All arguments are passed to `Amount.quantize`.
        """
        return Price(
            net=self.net.quantize(exp, rounding=rounding),
            gross=self.gross.quantize(exp, rounding=rounding))
