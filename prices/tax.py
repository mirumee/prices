from decimal import Decimal

from .price import Price
from .price_range import PriceRange

class Tax(object):
    """A generic tax class, provided so all taxers have a common base.
    """
    name = None

    def apply(self, other):
        if isinstance(other, Price):
            return Price(
                net=other.net,
                gross=other.gross + self.calculate_tax(other))
        elif isinstance(other, PriceRange):
            return PriceRange(
                self.apply(other.min_price), self.apply(other.max_price))
        else:
            raise TypeError('Cannot apply tax to %r' % (other,))

    def calculate_tax(self, price):
        """Calculate the tax amount.
        """
        raise NotImplementedError()


class LinearTax(Tax):
    """Adds a certain fraction on top of the price.
    """
    def __init__(self, multiplier, name=None):
        self.multiplier = Decimal(multiplier)
        self.name = name or self.name

    def __repr__(self):
        return 'LinearTax(%r, name=%r)' % (str(self.multiplier), self.name)

    def __lt__(self, other):
        if isinstance(other, LinearTax):
            return self.multiplier < other.multiplier
        return NotImplemented

    def __gt__(self, other):
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, LinearTax):
            return (
                self.multiplier == other.multiplier and
                self.name == other.name)
        return False

    def __ne__(self, other):
        return not self == other

    def calculate_tax(self, price):
        return price.net * self.multiplier
