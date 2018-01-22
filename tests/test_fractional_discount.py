from decimal import Decimal
from functools import partial

import pytest

from prices import Money, TaxedMoney, TaxedMoneyRange, fractional_discount


def test_discount():
    price = TaxedMoney(Money(100, 'BTC'), Money(100, 'BTC'))
    discount = partial(fractional_discount, fraction=Decimal('0.25'))
    result = discount(price)
    assert result.net == Money(75, 'BTC')
    assert result.gross == Money(75, 'BTC')
    price_range = TaxedMoneyRange(price, price)
    result = discount(price_range)
    assert result.start == TaxedMoney(Money(75, 'BTC'), Money(75, 'BTC'))
    assert result.stop == TaxedMoney(Money(75, 'BTC'), Money(75, 'BTC'))
    result = discount(Money(100, 'BTC'))
    assert result == Money(75, 'BTC')
    with pytest.raises(TypeError):
        discount(100)


def test_discount_from_net():
    price = TaxedMoney(Money(100, 'PLN'), Money(200, 'PLN'))
    result = fractional_discount(price, Decimal('0.5'), from_gross=False)
    assert result.net == Money(50, 'PLN')
    assert result.gross == Money(150, 'PLN')
