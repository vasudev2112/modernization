import unittest

class DiscountCalculator:
    @staticmethod
    def calculate_discount(amount: float, customer_type: str) -> float:
        discount = 0.0
        if customer_type.strip().upper() == "PREMIUM":
            discount = 0.20
        elif customer_type.strip().upper() == "STANDARD":
            discount = 0.10
        if amount > 10000:
            discount += 0.05
        final_amount = amount - (amount * discount)
        if final_amount < 0:
            final_amount = 0.0
        return final_amount

class TestDiscountCalculator(unittest.TestCase):
    def test_premium_standard(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(5000, "PREMIUM"), 4000.0)
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(15000, "STANDARD"), 12750.0)
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(2000, "UNKNOWN"), 2000.0)
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(15000, "PREMIUM"), 11250.0)
    def test_negative_and_zero(self):
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(-1000, "PREMIUM"), 0.0)
        self.assertAlmostEqual(DiscountCalculator.calculate_discount(0, "STANDARD"), 0.0)

if __name__ == "__main__":
    unittest.main()