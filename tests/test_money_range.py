import pytest

from prices import Money, MoneyRange


def test_construction():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range = MoneyRange(price1, price2)
    assert price_range.start == price1
    assert price_range.stop == price2
    with pytest.raises(ValueError):
        MoneyRange(price1, Money(20, 'PLN'))
    with pytest.raises(ValueError):
        MoneyRange(price2, price1)


def test_addition_with_money():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range = MoneyRange(price1, price2)
    price3 = Money(40, 'EUR')
    result = price_range + price3
    assert result.start == price1 + price3
    assert result.stop == price2 + price3
    with pytest.raises(ValueError):
        price_range + Money(1, 'BTC')


def test_addition_with_money_range():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range1 = MoneyRange(price1, price2)
    price3 = Money(40, 'EUR')
    price4 = Money(80, 'EUR')
    price_range2 = MoneyRange(price3, price4)
    result = price_range1 + price_range2
    assert result.start == price1 + price3
    assert result.stop == price2 + price4
    with pytest.raises(ValueError):
        price_range1 + MoneyRange(Money(1, 'BTC'), Money(2, 'BTC'))


def test_addition_with_other_types():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range = MoneyRange(price1, price2)
    with pytest.raises(TypeError):
        price_range + 1


def test_subtraction_with_money():
    price1 = Money(40, 'EUR')
    price2 = Money(80, 'EUR')
    price_range = MoneyRange(price1, price2)
    price3 = Money(10, 'EUR')
    result = price_range - price3
    assert result.start == price1 - price3
    assert result.stop == price2 - price3
    with pytest.raises(ValueError):
        price_range - Money(1, 'BTC')


def test_subtraction_with_money_range():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range1 = MoneyRange(price1, price2)
    price3 = Money(40, 'EUR')
    price4 = Money(80, 'EUR')
    price_range2 = MoneyRange(price3, price4)
    result = price_range2 - price_range1
    assert result.start == price3 - price1
    assert result.stop == price4 - price2
    with pytest.raises(ValueError):
        price_range2 - MoneyRange(Money(1, 'BTC'), Money(2, 'BTC'))


def test_subtraction_with_other_types():
    price1 = Money(40, 'EUR')
    price2 = Money(80, 'EUR')
    price_range = MoneyRange(price1, price2)
    with pytest.raises(TypeError):
        price_range - 1


def test_comparison():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range1 = MoneyRange(price1, price2)
    price3 = Money(40, 'EUR')
    price4 = Money(80, 'EUR')
    price_range2 = MoneyRange(price3, price4)
    assert price_range1 == MoneyRange(price1, price2)
    assert price_range1 != price_range2
    assert price_range1 != MoneyRange(price1, price1)
    assert price_range1 != MoneyRange(
        Money(10, 'USD'), Money(30, 'USD'))
    assert price_range1 != price1


def test_membership():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range = MoneyRange(price1, price2)
    assert price1 in price_range
    assert price2 in price_range
    assert (price1 + price2) / 2 in price_range
    assert price1 + price2 not in price_range
    with pytest.raises(TypeError):
        15 in price_range


def test_quantize():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range = MoneyRange(price1, price2)
    result = price_range.quantize()
    assert str(result.start.amount) == '10.00'
    assert str(result.stop.amount) == '30.00'


def test_replace():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price3 = Money(20, 'EUR')
    price_range = MoneyRange(price1, price2)
    result = price_range.replace(stop=price3)
    assert result.start == price1
    assert result.stop == price3
    result = price_range.replace(start=price3)
    assert result.start == price3
    assert result.stop == price2


def test_currency():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range = MoneyRange(price1, price2)
    assert price_range.currency == 'EUR'


def test_repr():
    price1 = Money(10, 'EUR')
    price2 = Money(30, 'EUR')
    price_range = MoneyRange(price1, price2)
    assert repr(price_range) == (
        "MoneyRange(Money('10', 'EUR'), Money('30', 'EUR'))")
