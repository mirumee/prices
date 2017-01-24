from prices import Amount, FractionalDiscount, Price, PriceRange


def test_discount():
    price = Price(Amount(100, 'BTC'), Amount(100, 'BTC'))
    discount = FractionalDiscount(factor='0.25')
    result = discount.apply(price)
    assert result.net == Amount(75, 'BTC')
    assert result.gross == Amount(75, 'BTC')
    price_range = PriceRange(price, price)
    result = discount.apply(price_range)
    assert result.min_price == Price(Amount(75, 'BTC'), Amount(75, 'BTC'))
    assert result.max_price == Price(Amount(75, 'BTC'), Amount(75, 'BTC'))


def test_repr():
    discount = FractionalDiscount(factor='0.25', name='Test discount')
    assert repr(discount) == (
        "FractionalDiscount(Decimal('0.25'), name='Test discount')")
