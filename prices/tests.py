import decimal
import operator
import unittest

from prices import (FixedDiscount, FractionalDiscount, History, LinearTax,
                    Price, PriceRange, inspect_price, percentage_discount)


class PriceTest(unittest.TestCase):

    def setUp(self):
        self.ten_btc = Price(10, currency='BTC')
        self.twenty_btc = Price(20, currency='BTC')
        self.thirty_dollars = Price(30, currency='USD')

    def test_basics(self):
        self.assertEqual(self.ten_btc.net, self.ten_btc.gross)

    def test_subtraction(self):
        res = self.twenty_btc - self.ten_btc
        self.assertEqual(res, Price(10, currency='BTC'))

    def test_invalid_subtraction(self):
        self.assertRaises(ValueError,
                          lambda: self.ten_btc - self.thirty_dollars)
        self.assertRaises(TypeError,
                          lambda: self.ten_btc - 1)

    def test_multiplication(self):
        p1 = self.ten_btc * 5
        self.assertEqual(p1.net, 50)
        self.assertEqual(p1.gross, 50)
        p2 = 5 * self.ten_btc
        self.assertEqual(p1, p2)

    def test_invalid_multiplication(self):
        self.assertRaises(TypeError,
                          lambda: self.ten_btc * self.twenty_btc)

    def test_division(self):
        p = self.ten_btc / 5
        self.assertEqual(p.net, 2)
        self.assertEqual(p.gross, 2)

    def test_equality(self):
        p1 = Price(net='10', gross='20', currency='USD')
        p2 = Price(net='10', gross='20', currency='USD')
        p3 = Price(net='20', gross='20', currency='USD')
        p4 = Price(net='10', gross='10', currency='USD')
        p5 = Price(net='10', gross='20', currency='AUD')
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        self.assertNotEqual(p1, p4)
        self.assertNotEqual(p1, p5)
        self.assertNotEqual(p1, 10)
        self.assertFalse(p1 != p2)

    def test_comparison(self):
        self.assertTrue(self.ten_btc < self.twenty_btc)
        self.assertTrue(self.ten_btc <= self.ten_btc)
        self.assertTrue(self.twenty_btc > self.ten_btc)
        self.assertTrue(self.ten_btc >= self.ten_btc)

    def test_invalid_comparison(self):
        self.assertRaises(ValueError,
                          lambda: self.ten_btc < self.thirty_dollars)
        self.assertRaises(ValueError,
                          lambda: self.ten_btc > self.thirty_dollars)

    def test_addition(self):
        p = self.ten_btc + self.twenty_btc
        self.assertEqual(p.net, 30)
        self.assertEqual(p.gross, 30)

    def test_invalid_addition(self):
        self.assertRaises(ValueError,
                          lambda: self.ten_btc + self.thirty_dollars)
        self.assertRaises(TypeError,
                          lambda: self.ten_btc + 1)

    def test_tax(self):
        p = Price(net='20', gross='30', currency='BTC')
        self.assertEqual(p.tax, 10)

    def test_inspect(self):
        p = ((self.ten_btc + self.twenty_btc) * 5 - self.ten_btc)
        p = p.quantize('0.01')
        self.assertEqual(
            inspect_price(p),
            "((((Price('10', currency='BTC') + Price('20', currency='BTC'))"
            " * 5) - Price('10', currency='BTC'))).quantize(Decimal('0.01'))")

    def test_elements(self):
        p1 = ((self.ten_btc + self.twenty_btc) * 5).quantize('0.01')
        self.assertEqual(
            list(p1.elements()),
            [self.ten_btc, self.twenty_btc, 5, decimal.Decimal('0.01')])
        p2 = Price(3, history=History(1, operator.__add__, 2))
        self.assertEqual(list(p2.elements()), [1, 2])

    def test_repr(self):
        p = Price(net='10', gross='20', currency='GBP')
        self.assertEqual(repr(p),
                         "Price(net='10', gross='20', currency='GBP')")


class PriceRangeTest(unittest.TestCase):

    def setUp(self):
        self.ten_btc = Price(10, currency='BTC')
        self.twenty_btc = Price(20, currency='BTC')
        self.thirty_btc = Price(30, currency='BTC')
        self.forty_btc = Price(40, currency='BTC')
        self.range_ten_twenty = PriceRange(self.ten_btc, self.twenty_btc)
        self.range_thirty_forty = PriceRange(self.thirty_btc, self.forty_btc)

    def test_basics(self):
        self.assertEqual(self.range_ten_twenty.min_price, self.ten_btc)
        self.assertEqual(self.range_ten_twenty.max_price, self.twenty_btc)

    def test_construction(self):
        pr = PriceRange(self.ten_btc)
        self.assertEqual(pr.min_price, self.ten_btc)
        self.assertEqual(pr.max_price, self.ten_btc)

    def test_invalid_construction(self):
        p = Price(10, currency='USD')
        self.assertRaises(ValueError, lambda: PriceRange(self.ten_btc, p))
        self.assertRaises(ValueError, lambda: PriceRange(self.twenty_btc,
                                                         self.ten_btc))

    def test_addition(self):
        pr1 = self.range_ten_twenty + self.range_thirty_forty
        self.assertEqual(pr1.min_price, self.ten_btc + self.thirty_btc)
        self.assertEqual(pr1.max_price, self.twenty_btc + self.forty_btc)
        pr2 = self.range_ten_twenty + self.ten_btc
        self.assertEqual(pr2.min_price, self.ten_btc + self.ten_btc)
        self.assertEqual(pr2.max_price, self.twenty_btc + self.ten_btc)

    def test_invalid_addition(self):
        p = Price(10, currency='USD')
        pr = PriceRange(p)
        self.assertRaises(ValueError, lambda: self.range_ten_twenty + pr)
        self.assertRaises(ValueError, lambda: self.range_ten_twenty + p)
        self.assertRaises(TypeError, lambda: self.range_ten_twenty + 10)

    def test_subtraction(self):
        pr1 = self.range_thirty_forty - self.range_ten_twenty
        pr2 = self.range_thirty_forty - self.ten_btc
        self.assertEqual(pr1.min_price, self.thirty_btc - self.ten_btc)
        self.assertEqual(pr1.max_price, self.forty_btc - self.twenty_btc)
        self.assertEqual(pr2.min_price, self.thirty_btc - self.ten_btc)
        self.assertEqual(pr2.max_price, self.forty_btc - self.ten_btc)

    def test_invalid_subtraction(self):
        p = Price(10, currency='USD')
        pr = PriceRange(p)
        self.assertRaises(ValueError, lambda: self.range_thirty_forty - pr)
        self.assertRaises(ValueError, lambda: self.range_thirty_forty - p)
        self.assertRaises(TypeError, lambda: self.range_thirty_forty - 1)

    def test_equality(self):
        pr1 = PriceRange(self.ten_btc, self.twenty_btc)
        pr2 = PriceRange(self.ten_btc, self.twenty_btc)
        pr3 = PriceRange(self.ten_btc, self.ten_btc)
        pr4 = PriceRange(self.twenty_btc, self.twenty_btc)
        self.assertEqual(pr1, pr2)
        self.assertNotEqual(pr1, pr3)
        self.assertNotEqual(pr1, pr4)
        self.assertNotEqual(pr1, self.ten_btc)
        self.assertFalse(pr1 != pr2)

    def test_membership(self):
        self.assertTrue(self.ten_btc in self.range_ten_twenty)
        self.assertTrue(self.twenty_btc in self.range_ten_twenty)
        self.assertFalse(self.thirty_btc in self.range_ten_twenty)

    def test_invalid_membership(self):
        self.assertRaises(TypeError, lambda: 15 in self.range_ten_twenty)

    def test_replacement(self):
        pr1 = self.range_ten_twenty.replace(max_price=self.thirty_btc)
        self.assertEqual(pr1.min_price, self.ten_btc)
        self.assertEqual(pr1.max_price, self.thirty_btc)
        pr2 = self.range_thirty_forty.replace(min_price=self.twenty_btc)
        self.assertEqual(pr2.min_price, self.twenty_btc)
        self.assertEqual(pr2.max_price, self.forty_btc)

    def test_repr(self):
        pr1 = self.range_thirty_forty
        pr2 = PriceRange(self.ten_btc, self.ten_btc)
        self.assertEqual(
            repr(pr1),
            "PriceRange(Price('30', currency='BTC'),"
            " Price('40', currency='BTC'))")
        self.assertEqual(
            repr(pr2),
            "PriceRange(Price('10', currency='BTC'))")

    def test_comparison(self):
        p10 = Price(10, currency='USD')
        p20 = Price(20, currency='USD')

        self.assertTrue(p10 < p20)
        self.assertTrue(p20 > p10)
        self.assertTrue(p10 <= p10)
        self.assertTrue(p10 >= p10)
        self.assertTrue(p10 == p10)


class LinearTaxTest(unittest.TestCase):

    def setUp(self):
        self.ten_btc = Price(10, currency='BTC')
        self.twenty_btc = Price(20, currency='BTC')
        self.range_ten_twenty = PriceRange(self.ten_btc, self.twenty_btc)

    def test_price(self):
        tax = LinearTax(1, name='2x Tax')
        p = self.ten_btc | tax
        self.assertEqual(p.net, self.ten_btc.net)
        self.assertEqual(p.gross, self.ten_btc.gross * 2)
        self.assertEqual(p.currency, self.ten_btc.currency)

    def test_pricerange(self):
        tax_name = '2x Tax'
        tax = LinearTax(1, name=tax_name)
        pr = self.range_ten_twenty | tax
        self.assertEqual(pr.min_price.net, self.ten_btc.net)
        self.assertEqual(pr.min_price.gross, self.ten_btc.gross * 2)
        self.assertEqual(pr.min_price.currency, self.ten_btc.currency)
        self.assertEqual(pr.max_price.net, self.twenty_btc.net)
        self.assertEqual(pr.max_price.gross, self.twenty_btc.gross * 2)
        self.assertEqual(pr.max_price.currency, self.twenty_btc.currency)

    def test_comparison(self):
        tax1 = LinearTax(1)
        tax2 = LinearTax(2)

        self.assertTrue(tax1 < tax2)
        self.assertTrue(tax2 > tax1)

    def test_equality(self):
        tax1 = LinearTax(1)
        tax2 = LinearTax(1)
        tax3 = LinearTax(2)
        self.assertEqual(tax1, tax2)
        self.assertNotEqual(tax1, tax3)
        self.assertNotEqual(tax1, 1)

    def test_repr(self):
        tax = LinearTax(decimal.Decimal('1.23'), name='VAT')
        self.assertEqual(repr(tax), "LinearTax('1.23', name='VAT')")


class FixedDiscountTest(unittest.TestCase):

    def test_discount(self):
        ten_btc = Price(10, currency='BTC')
        thirty_btc = Price(30, currency='BTC')
        discount = FixedDiscount(ten_btc, name='Ten off')
        p = thirty_btc | discount
        self.assertEqual(p.net, 20)
        self.assertEqual(p.gross, 20)
        self.assertEqual(p.currency, 'BTC')

    def test_zero_clipping(self):
        ten_btc = Price(10, currency='BTC')
        thirty_btc = Price(30, currency='BTC')
        discount = FixedDiscount(thirty_btc, name='Up to $30 OFF')
        p = ten_btc | discount
        self.assertEqual(p.net, 0)
        self.assertEqual(p.gross, 0)
        self.assertEqual(p.currency, 'BTC')

    def test_currency_mismatch(self):
        ten_btc = Price(10, currency='BTC')
        ten_usd = Price(10, currency='USD')
        discount = FixedDiscount(ten_usd)
        self.assertRaises(ValueError, lambda: ten_btc | discount)

    def test_repr(self):
        ten_usd = Price(10, currency='USD')
        discount = FixedDiscount(ten_usd, name='Ten off')
        self.assertEqual(
            repr(discount),
            "FixedDiscount(Price('10', currency='USD'), name='Ten off')")


class PercentageDiscountTest(unittest.TestCase):

    def test_discount(self):
        test_amount = Price(100, currency='BTC')
        discount = percentage_discount(value=10, name='Ten percent off')
        p = test_amount | discount
        self.assertEqual(p.net, 90)
        self.assertEqual(p.gross, 90)
        self.assertEqual(p.currency, 'BTC')

    def test_precision(self):
        test_amount = Price('1.01', currency='BTC')
        discount = percentage_discount(value=50, name='Half off')
        p = test_amount | discount
        self.assertEqual(p.net, decimal.Decimal('0.51'))
        self.assertEqual(p.net, decimal.Decimal('0.51'))
        self.assertEqual(p.currency, 'BTC')


class FractionalDiscountTest(unittest.TestCase):

    def setUp(self):
        self.test_amount = Price(100, currency='BTC')

    def test_discount(self):
        discount = FractionalDiscount(factor='0.25')
        p = self.test_amount | discount
        self.assertEqual(p.net, 75)
        self.assertEqual(p.gross, 75)
        self.assertEqual(p.currency, 'BTC')

    def test_repr(self):
        discount = FractionalDiscount(factor='0.25', name='Test discount')
        self.assertEqual(
            repr(discount),
            "FractionalDiscount(Decimal('0.25'), name='Test discount')")

if __name__ == '__main__':
    unittest.main()
