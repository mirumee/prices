# Prices: Python price handling for humans

[![codecov](https://codecov.io/github/mirumee/prices/graph/badge.svg?token=MPaL82nVJU)](https://codecov.io/github/mirumee/prices)
![PyPI - Version](https://img.shields.io/pypi/v/prices)
![PyPI - Downloads](https://img.shields.io/pypi/dm/prices)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/prices)

------

Money:

```python
from prices import Money
a = Money(10, 'USD')
a += Money(20, 'USD')
a.value
# Decimal('30')
a = a.quantize()
a.value
# Decimal('30.00')
a = Money('5.00', 'JPY')
a.quantize()
a.value
# Decimal('5')
```

Taxed money:

```python
from prices import Money, TaxedMoney
p = TaxedMoney(net=Money(20, 'EUR'), gross=Money(30, 'EUR'))
p.net
# Money('20', 'EUR')
p.gross
# Money('30', 'EUR')
p.tax
# Money('10', 'EUR')
p = p.quantize()
p.net
# Money('20.00', 'EUR')
```

Taxed ranges:

```python
from prices import Money, TaxedMoney, TaxedMoneyRange
price1 = TaxedMoney(Money(1, 'USD'), Money(1, 'USD'))
price2 = TaxedMoney(Money(10, 'USD'), Money(10, 'USD'))
pr = TaxedMoneyRange(price1, price2)
pr.min_price
# TaxedMoney(net=Money('1', 'USD'), gross=Money('1', 'USD'))
pr.max_price
# TaxedMoney(net=Money('10', 'USD'), gross=Money('10', 'USD'))
price3 = TaxedMoney(net=Money(5, 'USD'), gross=Money(5, 'USD'))
price3 in pr
# True
pr = pr.quantize()
pr.min_price.net
# Money('1.00', 'USD')
```

Taxes:

```python
from decimal import Decimal
from prices import Money, TaxedMoney, TaxedMoneyRange, flat_tax
p = TaxedMoney(Money('1.99', 'GBP'), Money('1.99', 'GBP'))
p = flat_tax(p, Decimal('0.23'))
p = p.quantize()
p.gross
# Money('2.45', 'GBP')
```

While protecting you from all sorts of mistakes:

```python
from prices import Money
Money(10, 'USD') < Money(15, 'GBP')
# ValueError: Cannot compare amounts in 'USD' and 'GBP'
```

```python
from prices import Money, TaxedMoney
price1 = TaxedMoney(Money(5, 'BTC'), Money(5, 'BTC'))
price2 = TaxedMoney(Money(7, 'INR'), Money(7, 'INR'))
price1 + price2
# ValueError: Cannot add amount in 'BTC' to 'INR'
```

## Prices ecosystem

| Repository | Description |
| ---------- | ----------- |
| [prices](https://github.com/mirumee/prices) | Python price handling for humans. |
| [django-prices](https://github.com/mirumee/django-prices) | Django fields for the `prices` module. |
| [django-prices-vatlayer](https://github.com/mirumee/django-prices-vatlayer) | Vatlayer API support for `django-prices`. |
| [django-prices-openexchangerates](https://github.com/mirumee/django-prices-openexchangerates) | openexchangerates.org support for `django-prices`. |

---

**Crafted with ❤️ by [Mirumee Software](http://mirumee.com)**

hello@mirumee.com
