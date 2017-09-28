Prices: Python price handling for humans
========================================

[![Build Status](https://secure.travis-ci.org/mirumee/prices.png)](https://travis-ci.org/mirumee/prices) [![codecov.io](http://codecov.io/github/mirumee/prices/coverage.svg?branch=master)](http://codecov.io/github/mirumee/prices?branch=master)

------

Amounts:

```python
from prices import Amount
a = Amount(10, 'USD')
a += Amount(20, 'USD')
a.value
# Decimal('30')
a = a.quantize()
a.value
# Decimal('30.00')
a = Amount('5.00', 'JPY')
a.quantize()
a.value
# Decimal('5')
```

Prices:

```python
from prices import Amount, Price
p = Price(net=Amount(20, 'EUR'), gross=Amount(30, 'EUR'))
p.net
# Amount('20', 'EUR')
p.gross
# Amount('30', 'EUR')
p.tax
# Amount('10', 'EUR')
p = p.quantize()
p.net
# Amount('20.00', 'EUR')
```

Price ranges:

```python
from prices import Amount, Price, PriceRange
price1 = Price(Amount(1, 'USD'), Amount(1, 'USD'))
price2 = Price(Amount(10, 'USD'), Amount(10, 'USD'))
pr = PriceRange(price1, price2)
pr.min_price
# Price(net=Amount('1', 'USD'), gross=Amount('1', 'USD'))
pr.max_price
# Price(net=Amount('10', 'USD'), gross=Amount('10', 'USD'))
price3 = Price(net=Amount(5, 'USD'), gross=Amount(5, 'USD'))
price3 in pr
# True
pr = pr.quantize()
pr.min_price.net
# Amount('1.00', 'USD')
```

Taxes:

```python
from prices import Price, PriceRange, LinearTax
p = Price(Amount('1.99', 'GBP'), Amount('1.99', 'GBP'))
tax = LinearTax('0.23', '23% VAT')
p = tax.apply(p)
p = p.quantize()
p.gross
# Amount('63.95', 'GBP')
```

While protecting you from all sorts of mistakes:

```python
from prices import Amount
Amount(10, 'USD') < Amount(15, 'GBP')
# ValueError: Cannot compare amounts in 'USD' and 'GBP'
```

```python
from prices import Amount, Price
price1 = Price(Amount(5, 'BTC'), Amount(5, 'BTC'))
price2 = Price(Amount(7, 'INR'), Amount(7, 'INR'))
price1 + price2
# ValueError: Cannot add amount in 'BTC' to 'INR'
```
