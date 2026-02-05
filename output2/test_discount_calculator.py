import unittest
from discount_calculator import DiscountCalculator

class TestDiscountCalculator(unittest.TestCase):
    def test_premium_low_amount(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(5000, "PREMIUM"), 4000.0)

    def test_standard_high_amount(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(15000, "STANDARD"), 12750.0)

    def test_unknown_customer(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(2000, "UNKNOWN"), 2000.0)

    def test_negative_final_amount(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(-5000, "PREMIUM"), 0.0)

    def test_zero_amount(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(0, "STANDARD"), 0.0)

    def test_edge_high_value(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(10000, "PREMIUM"), 8000.0)
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(10001, "PREMIUM"), 7500.75)

    def test_case_insensitivity(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(5000, "premium"), 4000.0)
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(5000, "STANDARD"), 4500.0)

    def test_whitespace_customer_type(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(5000, "  PREMIUM  "), 4000.0)

if __name__ == "__main__":
    unittest.main()
