from __future__ import division, unicode_literals

from .price import Price


class PriceRange(object):
    """A price range.
    """
    __slots__ = ('min_price', 'max_price')

    def __init__(self, min_price, max_price):
        if min_price.currency != max_price.currency:
            raise ValueError(
                'Cannot create a pricerange as %r and %r use different currencies' % (
                    min_price, max_price))
        if min_price > max_price:
            raise ValueError(
                'Cannot create a pricerange from %r to %r' % (
                    min_price, max_price))
        self.min_price = min_price
        self.max_price = max_price

    def __repr__(self):
        return 'PriceRange(%r, %r)' % (self.min_price, self.max_price)

    def __add__(self, other):
        if isinstance(other, Price):
            if other.currency != self.currency:
                raise ValueError(
                    "Cannot add pricerange in %r to price in %r" % (
                        self.currency, other.currency))
            min_price = self.min_price + other
            max_price = self.max_price + other
            return PriceRange(min_price=min_price, max_price=max_price)
        elif isinstance(other, PriceRange):
            if other.min_price.currency != self.currency:
                raise ValueError(
                    'Cannot add priceranges in %r and %r' % (
                        self.currency, other.currency))
            min_price = self.min_price + other.min_price
            max_price = self.max_price + other.max_price
            return PriceRange(min_price=min_price, max_price=max_price)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Price):
            if other.currency != self.min_price.currency:
                raise ValueError(
                    'Cannot subtract price in %r from pricerange in %r' % (
                        other.currency, self.min_price.currency))
            min_price = self.min_price - other
            max_price = self.max_price - other
            return PriceRange(min_price=min_price, max_price=max_price)
        elif isinstance(other, PriceRange):
            if other.min_price.currency != self.min_price.currency:
                raise ValueError(
                    'Cannot subtract pricerange in %r from %r' % (
                        other.min_price.currency, self.min_price.currency))
            min_price = self.min_price - other.min_price
            max_price = self.max_price - other.max_price
            return PriceRange(min_price=min_price, max_price=max_price)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, PriceRange):
            return (
                self.min_price == other.min_price and
                self.max_price == other.max_price)
        return False

    def __ne__(self, other):
        return not self == other

    def __contains__(self, item):
        if not isinstance(item, Price):
            raise TypeError(
                'in <pricerange> requires price as left operand, not %s' % (
                    type(item),))
        return self.min_price <= item <= self.max_price

    @property
    def currency(self):
        """Returns the currency of the price range.
        """
        return self.min_price.currency

    def quantize(self, exp=None, rounding=None):
        """Returns a quantized copy of the price range.

        All arguments are passed to `Price.quantize` which in turn calls
        `Amount.quantize`.
        """
        return PriceRange(
            self.min_price.quantize(exp, rounding=rounding),
            self.max_price.quantize(exp, rounding=rounding))

    def replace(self, min_price=None, max_price=None):
        """Return a new PriceRange object with one or more properties set to
        values passed to this method.
        """
        if min_price is None:
            min_price = self.min_price
        if max_price is None:
            max_price = self.max_price
        return PriceRange(min_price=min_price, max_price=max_price)
