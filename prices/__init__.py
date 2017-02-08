from collections import namedtuple
from decimal import Decimal, ROUND_HALF_UP
import operator
import warnings

CENTS = Decimal('.01')


class History(namedtuple('History', 'left operator right')):

    def __repr__(self):
        left = self.left.history if isinstance(self.left, Price) else None
        left = left or self.left
        right = self.right.history if isinstance(self.right, Price) else None
        right = right or self.right
        if self.operator is operator.__mul__:
            return '(%r * %r)' % (left, right)
        elif self.operator is operator.__truediv__:
            return '(%r / %r)' % (left, right)
        elif self.operator == Price.quantize:
            return '(%r).quantize(%r)' % (left, right)
        elif self.operator is operator.__sub__:
            return '(%r - %r)' % (left, right)
        elif self.operator is operator.__or__:
            return '(%r | %r)' % (left, right)
        return '(%r + %r)' % (left, right)


class Price(namedtuple('Price', 'net gross currency history')):

    def __new__(cls, net, gross=None, currency=None, history=None):
        if isinstance(net, float) or isinstance(gross, float):
            warnings.warn(  # pragma: no cover
                RuntimeWarning(
                    'You should never use floats when dealing with prices!'),
                stacklevel=2)
        net = Decimal(net)
        if gross is not None:
            gross = Decimal(gross)
        else:
            gross = net
        return super(Price, cls).__new__(cls, net, gross, currency, history)

    def __repr__(self):
        if self.net == self.gross:
            return 'Price(%r, currency=%r)' % (str(self.net), self.currency)
        return ('Price(net=%r, gross=%r, currency=%r)' %
                (str(self.net), str(self.gross), self.currency))

    def __lt__(self, other):
        if isinstance(other, Price):
            if self.currency != other.currency:
                raise ValueError('Cannot compare prices in %r and %r' %
                                 (self.currency, other.currency))
            return self.gross < other.gross
        return NotImplemented

    def __le__(self, other):
        if self == other:
            return True
        return self < other

    def __gt__(self, other):
        if isinstance(other, Price):
            if self.currency != other.currency:
                raise ValueError('Cannot compare prices in %r and %r' %
                                 (self.currency, other.currency))
            return self.gross > other.gross
        return NotImplemented

    def __ge__(self, other):
        if self == other:
            return True
        return self > other

    def __eq__(self, other):
        if isinstance(other, Price):
            return (self.gross == other.gross and
                    self.net == other.net and
                    self.currency == other.currency)
        return False

    def __ne__(self, other):
        return not self == other

    def __mul__(self, other):
        if isinstance(other, Price):
            raise TypeError('You can\'t multiply two Price objects')
        try:
            price_net = self.net * other
            price_gross = self.gross * other
        except TypeError:
            return NotImplemented
        history = History(self, operator.__mul__, other)
        return Price(net=price_net, gross=price_gross, currency=self.currency,
                     history=history)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        try:
            price_net = self.net / other
            price_gross = self.gross / other
        except TypeError:
            return NotImplemented
        history = History(self, operator.__truediv__, other)
        return Price(net=price_net, gross=price_gross, currency=self.currency,
                     history=history)

    def __div__(self, other):
        return self.__truediv__(other)

    def __add__(self, other):
        if isinstance(other, PriceModifier):
            warnings.warn("adding PriceModifiers will be removed in 0.6",
                          DeprecationWarning)
            return other.apply(self)
        if isinstance(other, Price):
            if other.currency != self.currency:
                raise ValueError('Cannot add price in %r to %r' %
                                 (self.currency, other.currency))
            price_net = self.net + other.net
            price_gross = self.gross + other.gross
            history = History(self, operator.__add__, other)
            return Price(net=price_net, gross=price_gross,
                         currency=self.currency, history=history)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Price):
            if other.currency != self.currency:
                raise ValueError('Cannot subtract prices in %r from %r' %
                                 (other.currency, self.currency))
            price_net = self.net - other.net
            price_gross = self.gross - other.gross
            history = History(self, operator.__sub__, other)
            return Price(net=price_net, gross=price_gross,
                         currency=self.currency, history=history)
        return NotImplemented

    @property
    def tax(self):
        return self.gross - self.net

    def quantize(self, exp, rounding=ROUND_HALF_UP):
        exp = Decimal(exp)
        history = History(self, Price.quantize, exp)
        return Price(net=self.net.quantize(exp, rounding=rounding),
                     gross=self.gross.quantize(exp, rounding=rounding),
                     currency=self.currency, history=history)

    def elements(self):
        if not self.history:
            yield self
        else:
            if hasattr(self.history.left, 'elements'):
                for el in self.history.left.elements():
                    yield el
            else:
                yield self.history.left
            if hasattr(self.history.right, 'elements'):
                for el in self.history.right.elements():
                    yield el
            else:
                yield self.history.right


class PriceRange(namedtuple('PriceRange', 'min_price max_price')):

    def __new__(cls, min_price, max_price=None):
        if max_price is None:
            max_price = min_price
        if min_price.currency != max_price.currency:
            raise ValueError('Cannot create a pricerange as %r and %r use'
                             ' different currencies' % (min_price, max_price))
        if min_price > max_price:
            raise ValueError('Cannot create a pricerange from %r to %r' %
                             (min_price, max_price))
        return super(PriceRange, cls).__new__(cls, min_price, max_price)

    def __repr__(self):
        if self.max_price == self.min_price:
            return 'PriceRange(%r)' % (self.min_price,)
        return 'PriceRange(%r, %r)' % (self.min_price, self.max_price)

    def __add__(self, other):
        if isinstance(other, PriceModifier):
            warnings.warn("adding PriceModifiers will be removed in 0.6",
                          DeprecationWarning)
            return PriceRange(min_price=other.apply(self.min_price),
                              max_price=other.apply(self.max_price))
        if isinstance(other, Price):
            if other.currency != self.min_price.currency:
                raise ValueError("Cannot add pricerange in %r to price in %r" %
                                 (self.min_price.currency, other.currency))
            min_price = self.min_price + other
            max_price = self.max_price + other
            return PriceRange(min_price=min_price, max_price=max_price)
        elif isinstance(other, PriceRange):
            if other.min_price.currency != self.min_price.currency:
                raise ValueError('Cannot add priceranges in %r and %r' %
                                 (self.min_price.currency,
                                  other.min_price.currency))
            min_price = self.min_price + other.min_price
            max_price = self.max_price + other.max_price
            return PriceRange(min_price=min_price, max_price=max_price)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Price):
            if other.currency != self.min_price.currency:
                raise ValueError("Cannot subtract price in %r from pricerange"
                                 " in %r" %
                                 (other.currency, self.min_price.currency))
            min_price = self.min_price - other
            max_price = self.max_price - other
            return PriceRange(min_price=min_price, max_price=max_price)
        elif isinstance(other, PriceRange):
            if other.min_price.currency != self.min_price.currency:
                raise ValueError('Cannot subtract pricerange in %r from %r' %
                                 (other.min_price.currency,
                                  self.min_price.currency))
            min_price = self.min_price - other.min_price
            max_price = self.max_price - other.max_price
            return PriceRange(min_price=min_price, max_price=max_price)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, PriceRange):
            return (self.min_price == other.min_price and
                    self.max_price == other.max_price)
        return False

    def __ne__(self, other):
        return not self == other

    def __contains__(self, item):
        if not isinstance(item, Price):
            raise TypeError('in <pricerange> requires price as left operand,'
                            ' not %s' % (type(item),))
        return self.min_price <= item <= self.max_price

    def replace(self, min_price=None, max_price=None):
        """
        Return a new PriceRange object with one or more properties set to
        values passed to this method.
        """
        if min_price is None:
            min_price = self.min_price
        if max_price is None:
            max_price = self.max_price
        return PriceRange(min_price=min_price, max_price=max_price)


class PriceModifier(object):

    name = None

    def __ror__(self, other):
        if isinstance(other, Price):
            return self.apply(other)
        elif isinstance(other, PriceRange):
            return PriceRange(
                min_price=self.apply(other.min_price),
                max_price=self.apply(other.max_price))
        else:
            return NotImplemented

    def apply(self, price):
        raise NotImplementedError()


class Tax(PriceModifier):
    """A generic tax class, provided so all taxers have a common base."""
    def apply(self, price_obj):
        history = History(price_obj, operator.__or__, self)
        return Price(net=price_obj.net,
                     gross=price_obj.gross + self.calculate_tax(price_obj),
                     currency=price_obj.currency, history=history)

    def calculate_tax(self, price_obj):
        raise NotImplementedError()


class LinearTax(Tax):
    """Adds a certain fraction on top of the price. """
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
            return (self.multiplier == other.multiplier and
                    self.name == other.name)
        return False

    def __ne__(self, other):
        return NotImplemented

    def calculate_tax(self, price_obj):
        return price_obj.gross * self.multiplier


class FixedDiscount(PriceModifier):
    """Reduces price by a fixed amount."""
    def __init__(self, amount, name=None):
        self.amount = amount
        self.name = name or self.name

    def __repr__(self):
        return 'FixedDiscount(%r, name=%r)' % (self.amount, self.name)

    def apply(self, price_obj):
        if price_obj.currency != self.amount.currency:
            raise ValueError('Cannot apply a discount in %r to a price in %r' %
                             (self.amount.currency, price_obj.currency))
        history = History(price_obj, operator.__or__, self)
        return Price(net=max(price_obj.net - self.amount.net, 0),
                     gross=max(price_obj.gross - self.amount.gross, 0),
                     currency=price_obj.currency, history=history)


class FractionalDiscount(PriceModifier):
    """Reduces price by a given fraction."""
    def __init__(self, factor, name=None):
        self.name = name or self.name
        self.factor = Decimal(factor)

    def __repr__(self):
        return 'FractionalDiscount(%r, name=%r)' % (self.factor, self.name)

    def apply(self, price_obj):
        history = History(price_obj, operator.__or__, self)
        net_discount = (price_obj.net * self.factor).quantize(CENTS)
        gross_discount = (price_obj.gross * self.factor).quantize(CENTS)
        return Price(net=price_obj.net - net_discount,
                     gross=price_obj.gross - gross_discount,
                     currency=price_obj.currency, history=history)


def percentage_discount(value, name=None):
    factor = Decimal(value) / 100
    return FractionalDiscount(factor, name)


def inspect_price(price_obj):
    return repr(price_obj.history or price_obj)
