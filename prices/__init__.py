from decimal import Decimal, ROUND_HALF_UP
import operator

__version__ = '2012.9.1'


class price(object):
    gross = Decimal('NaN')
    gross_base = Decimal('NaN')
    net = Decimal('NaN')
    net_base = Decimal('NaN')
    currency = None

    def __init__(self, net, gross=None, currency=None, previous=None,
                 modifier=None, operation=None):
        self.net = Decimal(net)
        if gross is not None:
            self.gross = Decimal(gross)
        else:
            self.gross = self.net
        self.currency = currency
        self.previous = previous
        self.modifier = modifier
        self.operation = operation

    def __repr__(self):
        if self.net == self.gross:
            return 'price(%r, currency=%r)' % (self.net, self.currency)
        return ('price(net=%r, gross=%r, currency=%r)' %
                (self.net, self.gross, self.currency))

    def __lt__(self, other):
        if isinstance(other, price):
            if self.currency != other.currency:
                raise ValueError('Cannot compare prices in %r and %r' %
                                 (self.currency, other.currency))
            return self.gross < other.gross
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __eq__(self, other):
        if isinstance(other, price):
            return (self.gross == other.gross and
                    self.net == other.net and
                    self.currency == other.currency)
        return False

    def __ne__(self, other):
        return not self == other

    def __mul__(self, other):
        price_net = self.net * other
        price_gross = self.gross * other
        return price(net=price_net, gross=price_gross, currency=self.currency,
                     previous=self, modifier=other, operation=operator.__mul__)

    def __add__(self, other):
        if isinstance(other, pricemodifier):
            return other.apply(self)
        if isinstance(other, price):
            if other.currency != self.currency:
                raise ValueError('Cannot add price in %r to %r' %
                                 (self.currency, other.currency))
            price_net = self.net + other.net
            price_gross = self.gross + other.gross
            return price(net=price_net, gross=price_gross,
                         currency=self.currency, previous=self, modifier=other,
                         operation=operator.__add__)
        return NotImplemented

    @property
    def tax(self):
        return self.gross - self.net

    def quantize(self, exp, rounding=ROUND_HALF_UP):
        exp = Decimal(exp)
        return price(net=self.net.quantize(exp, rounding=rounding),
                     gross=self.gross.quantize(exp, rounding=rounding),
                     currency=self.currency, previous=self, modifier=exp,
                     operation=price.quantize)

    def inspect(self):
        if self.previous:
            return (self.previous.inspect(), self.operation, self.modifier)
        return self

    def elements(self):
        if not self.previous:
            return [self]
        if hasattr(self.modifier, 'elements'):
            modifiers = self.modifier.elements()
        else:
            modifiers = [self.modifier]
        return self.previous.elements() + modifiers


class pricerange(object):

    min_price = None
    max_price = None

    def __init__(self, min_price, max_price=None):
        self.min_price = min_price
        if max_price is None:
            max_price = min_price
        if min_price > max_price:
            raise ValueError('Cannot create a pricerange from %r to %r' %
                             (min_price, max_price))
        if min_price.currency != max_price.currency:
            raise ValueError('Cannot create a pricerange as %r and %r use'
                             ' different currencies' % (min_price, max_price))
        self.max_price = max_price

    def __repr__(self):
        if self.max_price == self.min_price:
            return 'pricerange(%r)' % (self.min_price,)
        return ('pricerange(%r, %r)' %
                (self.min_price, self.max_price))

    def __add__(self, other):
        if isinstance(other, pricemodifier):
            return pricerange(min_price=other.apply(self.min_price),
                              max_price=other.apply(self.max_price))
        if isinstance(other, price):
            if other.currency != self.min_price.currency:
                raise ValueError("Cannot add pricerange in %r to price in %r" %
                                 (self.min_price.currency, other.currency))
            min_price = self.min_price + other
            max_price = self.max_price + other
            return pricerange(min_price=min_price, max_price=max_price)
        elif isinstance(other, pricerange):
            if other.min_price.currency != self.min_price.currency:
                raise ValueError('Cannot add priceranges in %r and %r' %
                                 (self.min_price.currency,
                                  other.min_price.currency))
            min_price = self.min_price + other.min_price
            max_price = self.max_price + other.max_price
            return pricerange(min_price=min_price, max_price=max_price)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, pricerange):
            return (self.min_price == other.min_price and
                    self.max_price == other.max_price)
        return False

    def __ne__(self, other):
        return not self == other

    def __contains__(self, item):
        if not isinstance(item, price):
            raise TypeError('in <pricerange> requires price as left operand,'
                            ' not %s' % (type(item),))
        return self.min_price <= item <= self.max_price

    def replace(self, min_price=None, max_price=None):
        '''
        Return a new pricerange object with one or more properties set to
        values passed to this method.
        '''
        if min_price is None:
            min_price = self.min_price
        if max_price is None:
            max_price = self.max_price
        return pricerange(min_price=min_price, max_price=max_price)


class pricemodifier(object):

    name = None
    net = Decimal('0')
    gross = Decimal('0')

    def apply(self, price):
        raise NotImplementedError()


class tax(pricemodifier):
    '''
    A generic tax class, provided so all taxers have a common base.
    '''
    name = None

    def apply(self, price_obj):
        return price(net=price_obj.net,
                     gross=self.calculate_gross(price_obj),
                     currency=price_obj.currency,
                     previous=price_obj,
                     modifier=self,
                     operation=operator.__add__)

    def calculate_gross(self, price_obj):
        raise NotImplementedError()


class lineartax(tax):
    '''
    A linear tax, modifies .
    '''
    def __init__(self, multiplier, name=None):
        self.multiplier = Decimal(multiplier)
        self.name = name or self.name

    def __repr__(self):
        return 'lineartax(%r, name=%r)' % (self.multiplier, self.name)

    def __lt__(self, other):
        if not isinstance(other, lineartax):
            raise TypeError('Cannot compare lineartax to %r' % (other,))
        return self.multiplier < other.multiplier

    def __eq__(self, other):
        if isinstance(other, lineartax):
            return (self.multiplier == other.multiplier and
                    self.name == other.name)
        return False

    def __ne__(self, other):
        return not self == other

    def calculate_gross(self, price_obj):
        return price_obj.gross * self.multiplier


def inspect_price(price_obj):
    def format_inspect(data):
        if isinstance(data, tuple):
            op1, op, op2 = data
            if op is operator.__mul__:
                return '(%s) * %r' % (format_inspect(op1), op2)
            if op == price.quantize:
                return '(%s).quantize(%r)' % (format_inspect(op1), op2)
            return '%s + %s' % (format_inspect(op1), format_inspect(op2))
        return repr(data)
    return format_inspect(price_obj.inspect())
