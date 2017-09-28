from prices import Amount, Price, PriceRange, percentage_discount


def test_discount():
    price = Price(Amount(100, 'BTC'), Amount(100, 'BTC'))
    discount = percentage_discount(value=10, name='Ten percent off')
    result = discount.apply(price)
    assert result.net == Amount(90, 'BTC')
    assert result.gross == Amount(90, 'BTC')
    price_range = PriceRange(price, price)
    result = discount.apply(price_range)
    assert result.min_price == Price(Amount(90, 'BTC'), Amount(90, 'BTC'))
    assert result.max_price == Price(Amount(90, 'BTC'), Amount(90, 'BTC'))


def test_precision():
    price = Price(Amount('1.01', 'BTC'), Amount('1.01', 'BTC'))
    discount = percentage_discount(value=50, name='Half off')
    result = discount.apply(price)
    assert result.net == Amount('0.51', 'BTC')
    assert result.net == Amount('0.51', 'BTC')
