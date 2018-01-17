import decimal

import pytest

from prices import Money, LinearTax, TaxedMoney, TaxedMoneyRange


def test_application():
    tax = LinearTax(1, name='2x Tax')
    result = tax.apply(TaxedMoney(Money(10, 'BTC'), Money(10, 'BTC')))
    assert result.net == Money(10, 'BTC')
    assert result.gross == Money(20, 'BTC')
    with pytest.raises(TypeError):
        tax.apply(1)


def test_pricerange():
    tax_name = '2x Tax'
    tax = LinearTax(1, name=tax_name)
    price_range = TaxedMoneyRange(
        TaxedMoney(Money(10, 'BTC'), Money(10, 'BTC')),
        TaxedMoney(Money(20, 'BTC'), Money(20, 'BTC')))
    result = tax.apply(price_range)
    assert result.start == TaxedMoney(Money(10, 'BTC'), Money(20, 'BTC'))
    assert result.stop == TaxedMoney(Money(20, 'BTC'), Money(40, 'BTC'))


def test_comparison():
    tax1 = LinearTax(1)
    tax2 = LinearTax(2)
    assert tax1 == LinearTax(1)
    assert tax1 != 1
    assert tax1 < tax2
    assert tax2 > tax1
    assert tax1 <= tax1
    assert tax1 <= tax2
    assert tax2 >= tax1
    assert tax2 >= tax2


def test_repr():
    tax = LinearTax(decimal.Decimal('1.23'), name='VAT')
    assert repr(tax) == "LinearTax('1.23', name='VAT')"
