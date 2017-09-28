import pytest

from prices import Amount, Price, PriceRange


def test_construction():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price_range = PriceRange(price1, price2)
    assert price_range.min_price == price1
    assert price_range.max_price == price2
    with pytest.raises(ValueError):
        PriceRange(price1, Price(Amount(20, 'PLN'), Amount(20, 'PLN')))
    with pytest.raises(ValueError):
        PriceRange(price2, price1)


def test_addition():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price_range1 = PriceRange(price1, price2)
    price3 = Price(Amount(40, 'EUR'), Amount(60, 'EUR'))
    price4 = Price(Amount(80, 'EUR'), Amount(120, 'EUR'))
    price_range2 = PriceRange(price3, price4)
    result = price_range1 + price_range2
    assert result.min_price == price1 + price3
    assert result.max_price == price2 + price4
    result = price_range1 + price3
    assert result.min_price == price1 + price3
    assert result.max_price == price2 + price3
    with pytest.raises(ValueError):
        price_range1 + PriceRange(
            Price(Amount(1, 'BTC'), Amount(1, 'BTC')),
            Price(Amount(2, 'BTC'), Amount(2, 'BTC')))
    with pytest.raises(ValueError):
        price_range1 + Price(Amount(1, 'BTC'), Amount(1, 'BTC'))
    with pytest.raises(TypeError):
        price_range1 + 1


def test_subtraction():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price_range1 = PriceRange(price1, price2)
    price3 = Price(Amount(40, 'EUR'), Amount(60, 'EUR'))
    price4 = Price(Amount(80, 'EUR'), Amount(120, 'EUR'))
    price_range2 = PriceRange(price3, price4)
    result = price_range2 - price_range1
    assert result.min_price == price3 - price1
    assert result.max_price == price4 - price2
    result = price_range2 - price1
    assert result.min_price == price3 - price1
    assert result.max_price == price4 - price1
    with pytest.raises(ValueError):
        price_range2 - PriceRange(
            Price(Amount(1, 'BTC'), Amount(1, 'BTC')),
            Price(Amount(2, 'BTC'), Amount(2, 'BTC')))
    with pytest.raises(ValueError):
        price_range2 - Price(Amount(1, 'BTC'), Amount(1, 'BTC'))
    with pytest.raises(TypeError):
        price_range2 - 1


def test_comparison():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price_range1 = PriceRange(price1, price2)
    price3 = Price(Amount(40, 'EUR'), Amount(60, 'EUR'))
    price4 = Price(Amount(80, 'EUR'), Amount(120, 'EUR'))
    price_range2 = PriceRange(price3, price4)
    assert price_range1 == PriceRange(price1, price2)
    assert price_range1 != price_range2
    assert price_range1 != PriceRange(price1, price1)
    assert price_range1 != PriceRange(
        Price(Amount(10, 'USD'), Amount(15, 'USD')),
        Price(Amount(30, 'USD'), Amount(45, 'USD')))
    assert price_range1 != price1


def test_membership():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price_range = PriceRange(price1, price2)
    assert price1 in price_range
    assert price2 in price_range
    assert (price1 + price2) / 2 in price_range
    assert price1 + price2 not in price_range
    with pytest.raises(TypeError):
        15 in price_range


def test_quantize():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price_range = PriceRange(price1, price2)
    result = price_range.quantize()
    assert str(result.min_price.net.value) == '10.00'
    assert str(result.max_price.net.value) == '30.00'


def test_replace():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price3 = Price(Amount(20, 'EUR'), Amount(30, 'EUR'))
    price_range = PriceRange(price1, price2)
    result = price_range.replace(max_price=price3)
    assert result.min_price == price1
    assert result.max_price == price3
    result = price_range.replace(min_price=price3)
    assert result.min_price == price3
    assert result.max_price == price2


def test_currency():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price_range = PriceRange(price1, price2)
    assert price_range.currency == 'EUR'


def test_repr():
    price1 = Price(Amount(10, 'EUR'), Amount(15, 'EUR'))
    price2 = Price(Amount(30, 'EUR'), Amount(45, 'EUR'))
    price_range = PriceRange(price1, price2)
    assert repr(price_range) == (
        "PriceRange(Price(net=Amount('10', 'EUR'), gross=Amount('15', 'EUR')), Price(net=Amount('30', 'EUR'), gross=Amount('45', 'EUR')))")
