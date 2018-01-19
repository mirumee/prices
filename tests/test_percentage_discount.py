from functools import partial

from prices import Money, TaxedMoney, TaxedMoneyRange, percentage_discount


def test_discount():
    price = TaxedMoney(Money(100, 'BTC'), Money(100, 'BTC'))
    discount = partial(percentage_discount, percentage=10)
    result = discount(price)
    assert result.net == Money(90, 'BTC')
    assert result.gross == Money(90, 'BTC')
    price_range = TaxedMoneyRange(price, price)
    result = discount(price_range)
    assert result.start == TaxedMoney(Money(90, 'BTC'), Money(90, 'BTC'))
    assert result.stop == TaxedMoney(Money(90, 'BTC'), Money(90, 'BTC'))


def test_precision():
    price = TaxedMoney(Money('1.01', 'BTC'), Money('1.01', 'BTC'))
    result = percentage_discount(price, percentage=50)
    assert result.net == Money('0.51', 'BTC')
    assert result.net == Money('0.51', 'BTC')
