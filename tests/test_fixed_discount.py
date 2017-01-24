import pytest

from prices import Amount, FixedDiscount, Price, PriceRange


def test_application():
    price = Price(Amount(30, 'BTC'), Amount(30, 'BTC'))
    discount = FixedDiscount(Amount(10, 'BTC'), name='Ten off')
    result = discount.apply(price)
    assert result.net == Amount(20, 'BTC')
    assert result.gross == Amount(20, 'BTC')
    price_range = PriceRange(price, price)
    result = discount.apply(price_range)
    assert result.min_price == Price(Amount(20, 'BTC'), Amount(20, 'BTC'))
    assert result.max_price == Price(Amount(20, 'BTC'), Amount(20, 'BTC'))
    with pytest.raises(TypeError):
        discount.apply(1)


def test_zero_clipping():
    price = Price(Amount(10, 'USD'), Amount(10, 'USD'))
    discount = FixedDiscount(Amount(30, 'USD'), name='Up to $30 OFF')
    result = discount.apply(price)
    assert result.net == Amount(0, 'USD')
    assert result.gross == Amount(0, 'USD')


def test_currency_mismatch():
    discount = FixedDiscount(Amount(10, 'USD'))
    with pytest.raises(ValueError):
        discount.apply(Price(Amount(10, 'BTC'), Amount(10, 'BTC')))


def test_repr():
    discount = FixedDiscount(Amount(10, 'USD'), name='Ten off')
    assert repr(discount) == (
        "FixedDiscount(Amount('10', 'USD'), name='Ten off')")
