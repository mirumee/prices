import decimal
import unittest

from prices import price, pricerange, lineartax, inspect_price


class PriceTest(unittest.TestCase):

    def setUp(self):
        self.ten_btc = price(10, currency='BTC')
        self.twenty_btc = price(20, currency='BTC')
        self.thirty_dollars = price(30, currency='USD')

    def test_basics(self):
        self.assertEqual(self.ten_btc.net, self.ten_btc.gross)

    def test_adding_non_price_object_fails(self):
        self.assertRaises(TypeError, lambda p: p + 10, self.ten_btc)

    def test_multiplication(self):
        p1 = self.ten_btc * 5
        self.assertEqual(p1.net, 50)
        self.assertEqual(p1.gross, 50)
        p2 = self.ten_btc * 5
        self.assertEqual(p1, p2)

    def test_valid_comparison(self):
        self.assertLess(self.ten_btc, self.twenty_btc)
        self.assertGreater(self.twenty_btc, self.ten_btc)

    def test_invalid_comparison(self):
        self.assertRaises(TypeError, lambda: self.ten_btc < 3)
        self.assertRaises(ValueError,
                          lambda: self.ten_btc < self.thirty_dollars)

    def test_valid_addition(self):
        p = self.ten_btc + self.twenty_btc
        self.assertEqual(p.net, 30)
        self.assertEqual(p.gross, 30)

    def test_invalid_addition(self):
        self.assertRaises(ValueError,
                          lambda: self.ten_btc + self.thirty_dollars)

    def test_tax(self):
        tax = lineartax(2, name='2x Tax')
        p = self.ten_btc + tax
        self.assertEqual(p.net, self.ten_btc.net)
        self.assertEqual(p.gross, self.ten_btc.gross * 2)
        self.assertEqual(p.currency, self.ten_btc.currency)

    def test_inspect(self):
        tax = lineartax('1.2345678', name='Silly Tax')
        p = ((self.ten_btc + self.twenty_btc) * 5 + tax).quantize('0.01')
        self.assertEqual(
            inspect_price(p),
            "((price(Decimal('10'), currency='BTC') + price(Decimal('20'), currency='BTC')) * 5 + lineartax(Decimal('1.2345678'), name='Silly Tax')).quantize(Decimal('0.01'))")

    def test_elements(self):
        tax = lineartax('1.2345678', name='Silly Tax')
        p = ((self.ten_btc + self.twenty_btc) * 5 + tax).quantize('0.01')
        self.assertEqual(
            p.elements(),
            [self.ten_btc, self.twenty_btc, 5, tax, decimal.Decimal('0.01')])


class PriceRangeTest(unittest.TestCase):

    def setUp(self):
        self.ten_btc = price(10, currency='BTC')
        self.twenty_btc = price(20, currency='BTC')
        self.thirty_btc = price(30, currency='BTC')
        self.forty_btc = price(40, currency='BTC')
        self.range_ten_twenty = pricerange(self.ten_btc, self.twenty_btc)
        self.range_thirty_forty = pricerange(self.thirty_btc, self.forty_btc)

    def test_basics(self):
        self.assertEqual(self.range_ten_twenty.min_price, self.ten_btc)
        self.assertEqual(self.range_ten_twenty.max_price, self.twenty_btc)

    def test_valid_addition(self):
        pr1 = self.range_ten_twenty + self.range_thirty_forty
        self.assertEqual(pr1.min_price, self.ten_btc + self.thirty_btc)
        self.assertEqual(pr1.max_price, self.twenty_btc + self.forty_btc)
        pr2 = self.range_ten_twenty + self.ten_btc
        self.assertEqual(pr2.min_price, self.ten_btc + self.ten_btc)
        self.assertEqual(pr2.max_price, self.twenty_btc + self.ten_btc)

    def test_invalid_addition(self):
        self.assertRaises(TypeError, lambda: self.range_ten_twenty + 10)

    def test_valid_membership(self):
        '''
        Prices can fit in a pricerange.
        '''
        self.assertTrue(self.ten_btc in self.range_ten_twenty)
        self.assertTrue(self.twenty_btc in self.range_ten_twenty)
        self.assertFalse(self.thirty_btc in self.range_ten_twenty)

    def test_invalid_membership(self):
        '''
        Non-prices can't fit in a pricerange.
        '''
        self.assertRaises(TypeError, lambda: 15 in self.range_ten_twenty)

    def test_replacement(self):
        pr1 = self.range_ten_twenty.replace(max_price=self.thirty_btc)
        self.assertEqual(pr1.min_price, self.ten_btc)
        self.assertEqual(pr1.max_price, self.thirty_btc)
        pr2 = self.range_thirty_forty.replace(min_price=self.twenty_btc)
        self.assertEqual(pr2.min_price, self.twenty_btc)
        self.assertEqual(pr2.max_price, self.forty_btc)

    def test_tax(self):
        tax_name = '2x Tax'
        tax = lineartax(2, name=tax_name)
        pr = self.range_ten_twenty + tax
        self.assertEqual(pr.min_price.net, self.ten_btc.net)
        self.assertEqual(pr.min_price.gross, self.ten_btc.gross * 2)
        self.assertEqual(pr.min_price.currency, self.ten_btc.currency)
        self.assertEqual(pr.max_price.net, self.twenty_btc.net)
        self.assertEqual(pr.max_price.gross, self.twenty_btc.gross * 2)
        self.assertEqual(pr.max_price.currency, self.twenty_btc.currency)


if __name__ == '__main__':
    unittest.main()
