import pytest

from prices import Money, TaxedMoney, sum


def test_construction():
    price = TaxedMoney(Money(1, 'EUR'), Money(1, 'EUR'))
    assert price.net == price.gross == Money(1, 'EUR')
    with pytest.raises(TypeError):
        TaxedMoney(1, 1)


def test_construction_different_currencies():
    with pytest.raises(ValueError):
        TaxedMoney(net=Money(1, 'USD'), gross=Money(2, 'EUR'))


def test_addition():
    price1 = TaxedMoney(Money(10, 'USD'), Money(15, 'USD'))
    price2 = TaxedMoney(Money(20, 'USD'), Money(30, 'USD'))
    assert price2 + price1 == TaxedMoney(Money(30, 'USD'), Money(45, 'USD'))
    result = price1 + Money(5, 'USD')
    assert result.net == Money(15, 'USD')
    assert result.gross == Money(20, 'USD')
    with pytest.raises(ValueError):
        price1 + TaxedMoney(Money(10, 'GBP'), Money(10, 'GBP'))
    with pytest.raises(TypeError):
        price1 + 1


def test_subtraction():
    price1 = TaxedMoney(Money(10, 'USD'), Money(15, 'USD'))
    price2 = TaxedMoney(Money(30, 'USD'), Money(45, 'USD'))
    assert price2 - price1 == TaxedMoney(Money(20, 'USD'), Money(30, 'USD'))
    result = price1 - Money(5, 'USD')
    assert result.net == Money(5, 'USD')
    assert result.gross == Money(10, 'USD')
    with pytest.raises(ValueError):
        price1 - TaxedMoney(Money(10, 'GBP'), Money(10, 'GBP'))
    with pytest.raises(TypeError):
        price1 - 1


def test_multiplication():
    price = TaxedMoney(Money(10, 'EUR'), Money(20, 'EUR'))
    assert price * 2 == TaxedMoney(Money(20, 'EUR'), Money(40, 'EUR'))
    assert 2 * price == price * 2
    with pytest.raises(TypeError):
        price * price


def test_division():
    price = TaxedMoney(Money(10, 'EUR'), Money(20, 'EUR'))
    assert price / 2 == TaxedMoney(Money(5, 'EUR'), Money(10, 'EUR'))
    with pytest.raises(TypeError):
        price / price


def test_comparison():
    price = TaxedMoney(Money(10, 'EUR'), Money(15, 'EUR'))
    assert price == TaxedMoney(Money(10, 'EUR'), Money(15, 'EUR'))
    assert price != TaxedMoney(Money(20, 'EUR'), Money(30, 'EUR'))
    assert price != TaxedMoney(Money(10, 'GBP'), Money(15, 'GBP'))
    assert price != Money(10, 'EUR')
    assert price < TaxedMoney(Money(20, 'EUR'), Money(30, 'EUR'))
    assert price <= TaxedMoney(Money(10, 'EUR'), Money(15, 'EUR'))
    assert price <= TaxedMoney(Money(20, 'EUR'), Money(30, 'EUR'))
    assert price > TaxedMoney(Money(1, 'EUR'), Money(1, 'EUR'))
    assert price >= TaxedMoney(Money(10, 'EUR'), Money(15, 'EUR'))
    assert price >= TaxedMoney(Money(1, 'EUR'), Money(1, 'EUR'))
    assert not price <= TaxedMoney(Money(1, 'EUR'), Money(1, 'EUR'))
    assert not price >= TaxedMoney(Money(20, 'EUR'), Money(30, 'EUR'))
    with pytest.raises(ValueError):
        price < TaxedMoney(Money(10, 'GBP'), Money(15, 'GBP'))
    with pytest.raises(TypeError):
        price >= Money(1, 'EUR')
    with pytest.raises(TypeError):
        price < Money(20, 'EUR')


def test_quantize():
    price = TaxedMoney(Money('1.001', 'EUR'), Money('1.001', 'EUR'))
    assert price.quantize() == (
        TaxedMoney(Money('1.00', 'EUR'), Money('1.00', 'EUR')))


def test_currency():
    price = TaxedMoney(Money(1, 'PLN'), Money(1, 'PLN'))
    assert price.currency == 'PLN'


def test_tax():
    price = TaxedMoney(Money(10, 'USD'), Money(15, 'USD'))
    assert price.tax == Money(5, 'USD')


def test_repr():
    price = TaxedMoney(Money(10, 'USD'), Money(15, 'USD'))
    assert repr(price) == (
        "TaxedMoney(net=Money('10', 'USD'), gross=Money('15', 'USD'))")


def test_sum():
    assert sum([Money(5, 'USD'), Money(10, 'USD')]) == Money(15, 'USD')
    with pytest.raises(TypeError):
        sum([])
