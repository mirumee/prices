from decimal import Decimal

import pytest

from prices import Money, MoneyRange, TaxedMoney, TaxedMoneyRange, flat_tax


def test_application():
    result = flat_tax(TaxedMoney(Money(10, 'BTC'), Money(10, 'BTC')), 1)
    assert result.net == Money(10, 'BTC')
    assert result.gross == Money(20, 'BTC')
    result = flat_tax(Money(100, 'BTC'), Decimal('0.5'))
    assert result.net == Money(100, 'BTC')
    assert result.gross == Money(150, 'BTC')
    with pytest.raises(TypeError):
        flat_tax(1, 1)


def test_tax_from_gross():
    result = flat_tax(
        TaxedMoney(Money(120, 'USD'), Money(120, 'USD')),
        Decimal('0.2'), keep_gross=True)
    assert result.net == Money(100, 'USD')
    assert result.gross == Money(120, 'USD')
    result = flat_tax(Money(150, 'BTC'), Decimal('0.5'), keep_gross=True)
    assert result.net == Money(100, 'BTC')
    assert result.gross == Money(150, 'BTC')


def test_range():
    price_range = MoneyRange(Money(10, 'BTC'), Money(20, 'BTC'))
    result = flat_tax(price_range, 1)
    assert result.start == TaxedMoney(Money(10, 'BTC'), Money(20, 'BTC'))
    assert result.stop == TaxedMoney(Money(20, 'BTC'), Money(40, 'BTC'))
    price_range = TaxedMoneyRange(
        TaxedMoney(Money(10, 'BTC'), Money(10, 'BTC')),
        TaxedMoney(Money(20, 'BTC'), Money(20, 'BTC')))
    result = flat_tax(price_range, 1)
    assert result.start == TaxedMoney(Money(10, 'BTC'), Money(20, 'BTC'))
    assert result.stop == TaxedMoney(Money(20, 'BTC'), Money(40, 'BTC'))
