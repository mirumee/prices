import pytest

from prices import FixedDiscount, Money, TaxedMoney, TaxedMoneyRange


def test_application():
    price = TaxedMoney(Money(30, 'BTC'), Money(30, 'BTC'))
    discount = FixedDiscount(Money(10, 'BTC'), name='Ten off')
    result = discount.apply(price)
    assert result.net == Money(20, 'BTC')
    assert result.gross == Money(20, 'BTC')
    price_range = TaxedMoneyRange(price, price)
    result = discount.apply(price_range)
    assert result.start == TaxedMoney(Money(20, 'BTC'), Money(20, 'BTC'))
    assert result.stop == TaxedMoney(Money(20, 'BTC'), Money(20, 'BTC'))
    with pytest.raises(TypeError):
        discount.apply(1)


def test_zero_clipping():
    price = TaxedMoney(Money(10, 'USD'), Money(10, 'USD'))
    discount = FixedDiscount(Money(30, 'USD'), name='Up to $30 OFF')
    result = discount.apply(price)
    assert result.net == Money(0, 'USD')
    assert result.gross == Money(0, 'USD')


def test_currency_mismatch():
    discount = FixedDiscount(Money(10, 'USD'))
    with pytest.raises(ValueError):
        discount.apply(TaxedMoney(Money(10, 'BTC'), Money(10, 'BTC')))


def test_repr():
    discount = FixedDiscount(Money(10, 'USD'), name='Ten off')
    assert repr(discount) == (
        "FixedDiscount(Money('10', 'USD'), name='Ten off')")
