import decimal

import pytest

from prices import Amount, LinearTax, Price, PriceRange


def test_application():
    tax = LinearTax(1, name='2x Tax')
    result = tax.apply(Price(Amount(10, 'BTC'), Amount(10, 'BTC')))
    assert result.net == Amount(10, 'BTC')
    assert result.gross == Amount(20, 'BTC')
    with pytest.raises(TypeError):
        tax.apply(1)


def test_pricerange():
    tax_name = '2x Tax'
    tax = LinearTax(1, name=tax_name)
    price_range = PriceRange(
        Price(Amount(10, 'BTC'), Amount(10, 'BTC')),
        Price(Amount(20, 'BTC'), Amount(20, 'BTC')))
    result = tax.apply(price_range)
    assert result.min_price == Price(Amount(10, 'BTC'), Amount(20, 'BTC'))
    assert result.max_price == Price(Amount(20, 'BTC'), Amount(40, 'BTC'))


def test_comparison():
    tax1 = LinearTax(1)
    tax2 = LinearTax(2)
    assert tax1 == LinearTax(1)
    assert tax1 != 1
    assert tax1 < tax2
    assert tax2 > tax1


def test_repr():
    tax = LinearTax(decimal.Decimal('1.23'), name='VAT')
    assert repr(tax) == "LinearTax('1.23', name='VAT')"
