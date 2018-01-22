from functools import partial

import pytest

from prices import (
    Money, MoneyRange, TaxedMoney, TaxedMoneyRange, fixed_discount)


def test_application():
    price = TaxedMoney(Money(30, 'BTC'), Money(30, 'BTC'))
    discount = partial(fixed_discount, discount=Money(10, 'BTC'))
    result = discount(price)
    assert result.net == Money(20, 'BTC')
    assert result.gross == Money(20, 'BTC')
    price_range = MoneyRange(price.net, price.net)
    result = discount(price_range)
    assert result.start == Money(20, 'BTC')
    assert result.stop == Money(20, 'BTC')
    price_range = TaxedMoneyRange(price, price)
    result = discount(price_range)
    assert result.start == TaxedMoney(Money(20, 'BTC'), Money(20, 'BTC'))
    assert result.stop == TaxedMoney(Money(20, 'BTC'), Money(20, 'BTC'))
    with pytest.raises(TypeError):
        discount(1)


def test_zero_clipping():
    price = TaxedMoney(Money(10, 'USD'), Money(10, 'USD'))
    result = fixed_discount(price, Money(30, 'USD'))
    assert result.net == Money(0, 'USD')
    assert result.gross == Money(0, 'USD')


def test_currency_mismatch():
    with pytest.raises(ValueError):
        fixed_discount(
            TaxedMoney(Money(10, 'BTC'), Money(10, 'BTC')),
            Money(10, 'USD'))
