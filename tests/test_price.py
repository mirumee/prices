import pytest

from prices import Amount, Price, sum


def test_construction():
    price = Price(Amount(1, 'EUR'), Amount(1, 'EUR'))
    assert price.net == price.gross == Amount(1, 'EUR')
    with pytest.raises(TypeError):
        Price(1, 1)


def test_construction_different_currencies():
    with pytest.raises(ValueError):
        Price(net=Amount(1, 'USD'), gross=Amount(2, 'EUR'))


def test_addition():
    price1 = Price(Amount(10, 'USD'), Amount(15, 'USD'))
    price2 = Price(Amount(20, 'USD'), Amount(30, 'USD'))
    assert price2 + price1 == Price(Amount(30, 'USD'), Amount(45, 'USD'))
    with pytest.raises(ValueError):
        price1 + Price(Amount(10, 'GBP'), Amount(10, 'GBP'))
    with pytest.raises(TypeError):
        price1 + 1


def test_subtraction():
    price1 = Price(Amount(10, 'USD'), Amount(15, 'USD'))
    price2 = Price(Amount(30, 'USD'), Amount(45, 'USD'))
    assert price2 - price1 == Price(Amount(20, 'USD'), Amount(30, 'USD'))
    with pytest.raises(ValueError):
        price1 - Price(Amount(10, 'GBP'), Amount(10, 'GBP'))
    with pytest.raises(TypeError):
        price1 - 1


def test_multiplication():
    price = Price(Amount(10, 'EUR'), Amount(20, 'EUR'))
    assert price * 2 == Price(Amount(20, 'EUR'), Amount(40, 'EUR'))
    assert 2 * price == price * 2
    with pytest.raises(TypeError):
        price * price


def test_division():
    price = Price(Amount(10, 'EUR'), Amount(20, 'EUR'))
    assert price / 2 == Price(Amount(5, 'EUR'), Amount(10, 'EUR'))
    with pytest.raises(TypeError):
        price / price


def test_comparison():
    price = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    assert price == Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    assert price != Price(Amount(20, 'EUR'), Amount(30, 'EUR'))
    assert price != Price(Amount(10, 'GBP'), Amount(15, 'GBP'))
    assert price != Amount(10, 'EUR')
    assert price < Price(Amount(20, 'EUR'), Amount(30, 'EUR'))
    assert price <= Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    assert price <= Price(Amount(20, 'EUR'), Amount(30, 'EUR'))
    assert price > Price(Amount(1, 'EUR'), Amount(1, 'EUR'))
    assert price >= Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    assert price >= Price(Amount(1, 'EUR'), Amount(1, 'EUR'))
    assert not price <= Price(Amount(1, 'EUR'), Amount(1, 'EUR'))
    assert not price >= Price(Amount(20, 'EUR'), Amount(30, 'EUR'))
    with pytest.raises(ValueError):
        price < Price(Amount(10, 'GBP'), Amount(15, 'GBP'))
    with pytest.raises(TypeError):
        price >= Amount(1, 'EUR')
    with pytest.raises(TypeError):
        price < Amount(20, 'EUR')


def test_quantize():
    price = Price(Amount('1.001', 'EUR'), Amount('1.001', 'EUR'))
    assert price.quantize() == (
        Price(Amount('1.00', 'EUR'), Amount('1.00', 'EUR')))


def test_currency():
    price = Price(Amount(1, 'PLN'), Amount(1, 'PLN'))
    assert price.currency == 'PLN'


def test_tax():
    price = Price(Amount(10, 'USD'), Amount(15, 'USD'))
    assert price.tax == Amount(5, 'USD')


def test_repr():
    price = Price(Amount(10, 'USD'), Amount(15, 'USD'))
    assert repr(price) == (
        "Price(net=Amount('10', 'USD'), gross=Amount('15', 'USD'))")


def test_sum():
    assert sum([Amount(5, 'USD'), Amount(10, 'USD')]) == Amount(15, 'USD')
    with pytest.raises(TypeError):
        sum([])
