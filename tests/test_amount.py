import pytest

from prices import Amount


def test_addition():
    amount = Amount(10, 'BTC') + Amount(20, 'BTC')
    assert amount.value == 30
    assert amount == Amount(30, 'BTC')
    with pytest.raises(ValueError):
        Amount(10, 'BTC') + Amount(30, 'USD')
    with pytest.raises(TypeError):
        Amount(10, 'USD') + 1


def test_subtraction():
    assert Amount(40, 'USD') - Amount(30, 'USD') == Amount(10, 'USD')
    with pytest.raises(ValueError):
        Amount(10, 'BTC') - Amount(30, 'USD')
    with pytest.raises(TypeError):
        Amount(10, 'BTC') - 1


def test_multiplication():
    amount = Amount(10, 'GBP') * 5
    assert amount.value == 50
    assert amount == 5 * Amount(10, 'GBP')
    with pytest.raises(TypeError):
        Amount(10, 'PLN') * Amount(10, 'PLN')
    with pytest.raises(TypeError):
        Amount(10, 'PLN') * None


def test_division():
    amount = Amount(10, 'EUR') / 5
    assert amount.value == 2
    assert Amount(10, 'USD') / Amount(2, 'USD') == 5
    with pytest.raises(ValueError):
        Amount(10, 'EUR') / Amount(5, 'GBP')


def test_comparison():
    assert Amount(10, 'USD') == Amount(10, 'USD')
    assert Amount(10, 'USD') != Amount(20, 'USD')
    assert Amount(10, 'USD') != Amount(10, 'EUR')
    assert Amount(10, 'USD') != 10
    assert Amount(10, 'USD') < Amount(20, 'USD')
    assert Amount(10, 'USD') <= Amount(10, 'USD')
    assert Amount(10, 'USD') <= Amount(20, 'USD')
    assert Amount(20, 'GBP') > Amount(10, 'GBP')
    assert Amount(10, 'GBP') >= Amount(10, 'GBP')
    assert Amount(20, 'GBP') >= Amount(10, 'GBP')
    assert not Amount(10, 'GBP') <= Amount(1, 'GBP')
    assert not Amount(1, 'GBP') >= Amount(10, 'GBP')
    with pytest.raises(ValueError):
        Amount(10, 'USD') > Amount(10, 'GBP')
    with pytest.raises(ValueError):
        Amount(10, 'USD') <= Amount(10, 'GBP')


def test_quantize():
    assert str(Amount(1, 'USD').quantize().value) == '1.00'
    assert str(Amount(1, 'JPY').quantize().value) == '1'
    assert str(Amount(1, 'USD').quantize('0.1').value) == '1.0'


def test_repr():
    amount = Amount(10, 'USD')
    assert repr(amount) == "Amount('10', 'USD')"
