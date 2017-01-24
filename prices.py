"""prices

Provides a Pythonic interface to deal with amounts, prices and taxes.
"""
from __future__ import division, unicode_literals

from collections import namedtuple
from decimal import Decimal, ROUND_HALF_UP
import functools
import operator
import warnings

import babel.core
import typing


class Amount(namedtuple('Amount', 'value currency')):
    """An amount of particular currency.
    """
    def __new__(cls, value, currency):
        # type: (Decimal, str) -> Amount
        if isinstance(value, float):
            warnings.warn(  # pragma: no cover
                RuntimeWarning(
                    'float passed as value to Amount, consider using Decimal'),
                stacklevel=2)
        value = Decimal(value)
        return super(Amount, cls).__new__(cls, value, currency)

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
        if self.__lt__(other):
            return True
        if self == other:
            return True
        return False

    def __gt__(self, other):
        if isinstance(other, Amount):
            if self.currency != other.currency:
                raise ValueError(
                    'Cannot compare amounts in %r and %r' % (
                        self.currency, other.currency))
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if self.__gt__(other):
            return True
        if self == other:
            return True
        return False

    def __eq__(self, other):
        if isinstance(other, Amount):
            return (
                self.value == other.value and
                self.currency == other.currency)
        return False

    def __ne__(self, other):
        return not self == other

    def __mul__(self, other):
        if isinstance(other, (Amount, Price)):
            raise TypeError(
                "Cannot multiply amount by %r" % (other,))
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

    def quantize(self, exp=None, rounding=ROUND_HALF_UP):
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


class Price(namedtuple('Price', 'net gross')):
    """A price, provides amounts for net, gross (incl. tax) and tax.
    """
    def __new__(cls, net, gross):
        if not isinstance(net, Amount) or not isinstance(gross, Amount):
            raise TypeError('Price requires two amounts, got %r, %r' % (
                net, gross))
        return super(Price, cls).__new__(cls, net, gross)

    def __repr__(self):
        return 'Price(net=%r, gross=%r)' % (self.net, self.gross)

    def __lt__(self, other):
        if isinstance(other, Price):
            return self.gross < other.gross
        elif isinstance(other, Amount):
            raise TypeError('Cannot compare prices and amounts')
        return NotImplemented

    def __le__(self, other):
        print('WOO', self, other)
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
        if isinstance(other, Price):
            raise TypeError('Cannot multiply two Price objects')
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

    def quantize(self, exp=None, rounding=ROUND_HALF_UP):
        """Quantizes the price to given precision.
        """
        return Price(
            net=self.net.quantize(exp, rounding=rounding),
            gross=self.gross.quantize(exp, rounding=rounding))


class PriceRange(namedtuple('PriceRange', 'min_price max_price')):
    """A price range.
    """
    def __new__(cls, min_price, max_price):
        # type: (Price, Price) -> PriceRange
        if not isinstance(min_price, Price) or not isinstance(max_price, Price):
            raise TypeError('PriceRange takes two prices, got %r, %r' % (
                min_price, max_price))
        if min_price.currency != max_price.currency:
            raise ValueError(
                'Cannot create a pricerange as %r and %r use different currencies' % (
                    min_price, max_price))
        if min_price > max_price:
            raise ValueError(
                'Cannot create a pricerange from %r to %r' % (
                    min_price, max_price))
        return super(PriceRange, cls).__new__(cls, min_price, max_price)

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
        # type: () -> str
        return self.min_price.currency


    def quantize(self, exp=None, rounding=ROUND_HALF_UP):
        """Quantizes the prices to given precision.
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


Modifiable = typing.Union[Price, PriceRange]


class Tax(object):
    """A generic tax class, provided so all taxers have a common base.
    """
    name = None  # type: str

    def apply(self, other):
        # type: (Modifiable) -> Modifiable
        if isinstance(other, Price):
            return Price(
                net=other.net,
                gross=other.gross + self.calculate_tax(other))
        elif isinstance(other, PriceRange):
            return PriceRange(
                self.apply(other.min_price), self.apply(other.max_price))
        else:
            raise TypeError('Cannot apply tax to %r' % (other,))

    def calculate_tax(self, price_obj):
        """Calculate the tax amount.
        """
        # type: (Price) -> Amount
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

    def calculate_tax(self, price_obj):
        # type: (Price) -> Amount
        return price_obj.net * self.multiplier


class Discount(object):
    """Base discount class.
    """
    name = None  # type: str

    def apply(self, other):
        """Apply the discount to a price or price range and return the
        discounted price.
        """
        # type: (Modifiable) -> Modifiable
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
        # type: (Price) -> Price
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
        # type: (Price) -> Price
        net_discount = price.net * self.factor
        gross_discount = price.gross * self.factor
        return Price(
            net=(price.net - net_discount).quantize(),
            gross=(price.gross - gross_discount).quantize())


def percentage_discount(value, name=None):
    """Returns a fractional discount given a percentage instead of a fraction.
    """
    # type: (decimal, str) -> FractionalDiscount
    factor = Decimal(value) / 100
    return FractionalDiscount(factor, name)


def sum(values):
    """Returns a sum of given values.
    """
    return functools.reduce(operator.add, values)
