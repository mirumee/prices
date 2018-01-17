from prices import FractionalDiscount, Money, TaxedMoney, TaxedMoneyRange


def test_discount():
    price = TaxedMoney(Money(100, 'BTC'), Money(100, 'BTC'))
    discount = FractionalDiscount(factor='0.25')
    result = discount.apply(price)
    assert result.net == Money(75, 'BTC')
    assert result.gross == Money(75, 'BTC')
    price_range = TaxedMoneyRange(price, price)
    result = discount.apply(price_range)
    assert result.start == TaxedMoney(Money(75, 'BTC'), Money(75, 'BTC'))
    assert result.stop == TaxedMoney(Money(75, 'BTC'), Money(75, 'BTC'))


def test_repr():
    discount = FractionalDiscount(factor='0.25', name='Test discount')
    assert repr(discount) == (
        "FractionalDiscount(Decimal('0.25'), name='Test discount')")
