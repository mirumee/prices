from decimal import Decimal

from .amount import Amount
from .price import Price
from .price_range import PriceRange


class Discount(object):
    """Base discount class.
    """
    name = None

    def apply(self, other):
        """Apply the discount to a price or price range and return the
        discounted price.
        """
        if isinstance(other, Price):
            return self.calculate_price(other)
        elif isinstance(other, PriceRange):
            return PriceRange(
                self.apply(other.min_price), self.apply(other.max_price))
        else:
            raise TypeError('Cannot apply discount to %r' % (other,))

    def calculate_price(self, price):
        """Calculate the price after discount.
        """
        raise NotImplementedError()


class FixedDiscount(Discount):
    """Reduces price by a fixed amount.
    """
    def __init__(self, amount, name=None):
        self.amount = amount
        self.name = name or self.name

    def __repr__(self):
        return 'FixedDiscount(%r, name=%r)' % (self.amount, self.name)

    def calculate_price(self, price):
        if price.currency != self.amount.currency:
            raise ValueError('Cannot apply a discount in %r to a price in %r' %
                             (self.amount.currency, price.currency))
        price_net = max(
            price.net - self.amount, Amount(0, self.amount.currency))
        price_gross = max(
            price.gross - self.amount, Amount(0, self.amount.currency))
        return Price(net=price_net, gross=price_gross)


class FractionalDiscount(Discount):
    """Reduces price by a given fraction.
    """
    def __init__(self, factor, name=None):
        self.name = name or self.name
        self.factor = Decimal(factor)

    def __repr__(self):
        return 'FractionalDiscount(%r, name=%r)' % (self.factor, self.name)

    def calculate_price(self, price):
        net_discount = price.net * self.factor
        gross_discount = price.gross * self.factor
        return Price(
            net=(price.net - net_discount).quantize(),
            gross=(price.gross - gross_discount).quantize())


def percentage_discount(value, name=None):
    """Returns a fractional discount given a percentage instead of a fraction.
    """
    factor = Decimal(value) / 100
    return FractionalDiscount(factor, name)
