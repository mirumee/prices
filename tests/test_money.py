from decimal import ROUND_DOWN

import pytest

from prices import Money


def test_addition():
    money = Money(10, 'BTC') + Money(20, 'BTC')
    assert money.amount == 30
    assert money == Money(30, 'BTC')
    with pytest.raises(ValueError):
        Money(10, 'BTC') + Money(30, 'USD')
    with pytest.raises(TypeError):
        Money(10, 'USD') + 1


def test_truthiness():
    money = Money(0, 'USD')
    assert bool(money) is False
    money = Money(1, 'USD')
    assert bool(money) is True


def test_subtraction():
    assert Money(40, 'USD') - Money(30, 'USD') == Money(10, 'USD')
    with pytest.raises(ValueError):
        Money(10, 'BTC') - Money(30, 'USD')
    with pytest.raises(TypeError):
        Money(10, 'BTC') - 1


def test_multiplication():
    money = Money(10, 'GBP') * 5
    assert money.amount == 50
    assert money == 5 * Money(10, 'GBP')
    with pytest.raises(TypeError):
        Money(10, 'PLN') * None


def test_division():
    money = Money(10, 'EUR') / 5
    assert money.amount == 2
    assert Money(10, 'USD') / Money(2, 'USD') == 5
    with pytest.raises(ValueError):
        Money(10, 'EUR') / Money(5, 'GBP')


def test_comparison():
    assert Money(10, 'USD') == Money(10, 'USD')
    assert Money(10, 'USD') != Money(20, 'USD')
    assert Money(10, 'USD') != Money(10, 'EUR')
    assert Money(10, 'USD') != 10
    assert Money(10, 'USD') < Money(20, 'USD')
    assert Money(10, 'USD') <= Money(10, 'USD')
    assert Money(10, 'USD') <= Money(20, 'USD')
    assert Money(20, 'GBP') > Money(10, 'GBP')
    assert Money(10, 'GBP') >= Money(10, 'GBP')
    assert Money(20, 'GBP') >= Money(10, 'GBP')
    assert not Money(10, 'GBP') <= Money(1, 'GBP')
    assert not Money(1, 'GBP') >= Money(10, 'GBP')
    with pytest.raises(ValueError):
        Money(10, 'USD') > Money(10, 'GBP')
    with pytest.raises(ValueError):
        Money(10, 'USD') <= Money(10, 'GBP')


def test_quantize():
    assert str(Money(1, 'USD').quantize().amount) == '1.00'
    assert str(Money(1, 'JPY').quantize().amount) == '1'
    assert str(Money(1, 'USD').quantize('0.1').amount) == '1.0'
    assert str(Money('1.9', 'JPY').quantize().amount) == '2'
    assert str(Money('1.9', 'JPY').quantize(rounding=ROUND_DOWN).amount) == '1'


def test_repr():
    money = Money(10, 'USD')
    assert repr(money) == "Money('10', 'USD')"
