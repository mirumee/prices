Prices: Python price handling for humans
========================================

[![Build Status](https://secure.travis-ci.org/mirumee/prices.png)](https://travis-ci.org/mirumee/prices) [![Coverage](https://coveralls.io/repos/mirumee/prices/badge.png)](https://coveralls.io/r/mirumee/prices)

------

```python
from prices import Price, PriceRange, LinearTax
p = Price('1.99')
p += Price(50)
p += LinearTax('0.23', '23% VAT')
print p.quantize('0.01').gross
# Decimal('63.95')
pr = PriceRange(Price(50), Price(100))
print p in pr
# True
```

While protecting you from all sorts of mistakes:

```python
Price(10, currency='USD') < Price(15, currency='GBP')
# ValueError: Cannot compare prices in 'USD' and 'GBP'
```

```python
Price(5, currency='BTC') + Price(7, currency='INR')
# ValueError: Cannot add price in 'BTC' to 'INR'
```

And being helpful:

```python
from prices import Price, LinearTax, inspect_price
p = Price('1.99')
p += Price(50)
p |= LinearTax('0.23', '23% VAT')
print inspect_price(p)
# "Price('1.99', currency=None) + Price('50', currency=None) | LinearTax('0.23', name='23% VAT')"
```
