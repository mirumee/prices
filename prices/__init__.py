"""prices.

Provides a Pythonic interface to deal with money types such as money amounts,
prices, discounts and taxes.
"""

from prices.discount import fixed_discount, fractional_discount, percentage_discount
from prices.money import Money
from prices.money_range import MoneyRange
from prices.tax import flat_tax
from prices.taxed_money import TaxedMoney
from prices.taxed_money_range import TaxedMoneyRange
from prices.utils import sum

__all__ = [
    "Money",
    "MoneyRange",
    "TaxedMoney",
    "TaxedMoneyRange",
    "fixed_discount",
    "flat_tax",
    "fractional_discount",
    "percentage_discount",
    "sum",
]
