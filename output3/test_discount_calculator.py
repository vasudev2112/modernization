"""Unit tests for the DiscountCalculator module.

This test suite provides comprehensive coverage of the discount calculation
functionality, including edge cases, boundary conditions, and error scenarios.

Author: Automated Java to Python Migration Agent
Date: 2024
"""

import unittest
from discount_calculator import DiscountCalculator


class TestDiscountCalculator(unittest.TestCase):
    """Test suite for DiscountCalculator class."""

    def test_premium_customer_basic_purchase(self):
        """Test premium customer with basic purchase amount."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        self.assertEqual(result, 4000.0)
        self.assertIsInstance(result, float)

    def test_standard_customer_basic_purchase(self):
        """Test standard customer with basic purchase amount."""
        result = DiscountCalculator.calculate_discount(5000, "STANDARD")
        self.assertEqual(result, 4500.0)
        self.assertIsInstance(result, float)

    def test_standard_customer_high_value_purchase(self):
        """Test standard customer with high-value purchase."""
        result = DiscountCalculator.calculate_discount(15000, "STANDARD")
        self.assertEqual(result, 12750.0)
        self.assertIsInstance(result, float)

    def test_premium_customer_high_value_purchase(self):
        """Test premium customer with high-value purchase."""
        result = DiscountCalculator.calculate_discount(12000, "PREMIUM")
        self.assertEqual(result, 9000.0)
        self.assertIsInstance(result, float)

    def test_unknown_customer_type(self):
        """Test unknown customer type receives no discount."""
        result = DiscountCalculator.calculate_discount(2000, "UNKNOWN")
        self.assertEqual(result, 2000.0)

    def test_empty_customer_type(self):
        """Test empty customer type receives no discount."""
        result = DiscountCalculator.calculate_discount(2000, "")
        self.assertEqual(result, 2000.0)

    def test_case_insensitive_premium(self):
        """Test customer type is case-insensitive for PREMIUM."""
        result1 = DiscountCalculator.calculate_discount(5000, "premium")
        result2 = DiscountCalculator.calculate_discount(5000, "Premium")
        result3 = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        result4 = DiscountCalculator.calculate_discount(5000, "PrEmIuM")
        
        self.assertEqual(result1, 4000.0)
        self.assertEqual(result2, 4000.0)
        self.assertEqual(result3, 4000.0)
        self.assertEqual(result4, 4000.0)

    def test_case_insensitive_standard(self):
        """Test customer type is case-insensitive for STANDARD."""
        result1 = DiscountCalculator.calculate_discount(5000, "standard")
        result2 = DiscountCalculator.calculate_discount(5000, "Standard")
        result3 = DiscountCalculator.calculate_discount(5000, "STANDARD")
        
        self.assertEqual(result1, 4500.0)
        self.assertEqual(result2, 4500.0)
        self.assertEqual(result3, 4500.0)

    def test_zero_amount(self):
        """Test zero purchase amount."""
        result = DiscountCalculator.calculate_discount(0, "PREMIUM")
        self.assertEqual(result, 0.0)

    def test_small_amount(self):
        """Test very small purchase amount."""
        result = DiscountCalculator.calculate_discount(0.01, "PREMIUM")
        self.assertAlmostEqual(result, 0.008, places=3)

    def test_high_value_threshold_exact(self):
        """Test purchase amount exactly at high-value threshold."""
        # Exactly 10000 - should NOT get high-value bonus
        result = DiscountCalculator.calculate_discount(10000, "PREMIUM")
        self.assertEqual(result, 8000.0)  # 20% discount only

    def test_high_value_threshold_just_above(self):
        """Test purchase amount just above high-value threshold."""
        # Just above 10000 - should get high-value bonus
        result = DiscountCalculator.calculate_discount(10001, "PREMIUM")
        self.assertAlmostEqual(result, 7500.75, places=2)  # 25% discount

    def test_high_value_threshold_just_below(self):
        """Test purchase amount just below high-value threshold."""
        # Just below 10000 - should NOT get high-value bonus
        result = DiscountCalculator.calculate_discount(9999, "PREMIUM")
        self.assertAlmostEqual(result, 7999.2, places=2)  # 20% discount only

    def test_large_amount(self):
        """Test very large purchase amount."""
        result = DiscountCalculator.calculate_discount(1000000, "PREMIUM")
        self.assertEqual(result, 750000.0)  # 25% discount

    def test_premium_discount_percentage(self):
        """Test premium discount is exactly 20%."""
        amount = 10000
        result = DiscountCalculator.calculate_discount(amount, "PREMIUM")
        discount_applied = amount - result
        discount_percentage = (discount_applied / amount) * 100
        self.assertAlmostEqual(discount_percentage, 20.0, places=2)

    def test_standard_discount_percentage(self):
        """Test standard discount is exactly 10%."""
        amount = 10000
        result = DiscountCalculator.calculate_discount(amount, "STANDARD")
        discount_applied = amount - result
        discount_percentage = (discount_applied / amount) * 100
        self.assertAlmostEqual(discount_percentage, 10.0, places=2)

    def test_high_value_bonus_percentage(self):
        """Test high-value bonus is exactly 5%."""
        amount = 20000
        result_premium = DiscountCalculator.calculate_discount(amount, "PREMIUM")
        discount_applied = amount - result_premium
        discount_percentage = (discount_applied / amount) * 100
        self.assertAlmostEqual(discount_percentage, 25.0, places=2)  # 20% + 5%

    def test_negative_amount_handling(self):
        """Test negative amount is handled correctly."""
        # The original Java code would calculate negative amounts
        # Python version maintains same behavior
        result = DiscountCalculator.calculate_discount(-1000, "PREMIUM")
        # Should return 0 due to negative check
        self.assertEqual(result, 0.0)

    def test_float_amount(self):
        """Test floating-point purchase amount."""
        result = DiscountCalculator.calculate_discount(5000.50, "PREMIUM")
        self.assertAlmostEqual(result, 4000.40, places=2)

    def test_integer_amount(self):
        """Test integer purchase amount."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        self.assertEqual(result, 4000.0)
        self.assertIsInstance(result, float)

    def test_multiple_calculations_independence(self):
        """Test multiple calculations don't affect each other."""
        result1 = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        result2 = DiscountCalculator.calculate_discount(3000, "STANDARD")
        result3 = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        
        self.assertEqual(result1, result3)  # Same inputs = same outputs
        self.assertNotEqual(result1, result2)  # Different inputs = different outputs

    def test_whitespace_in_customer_type(self):
        """Test customer type with whitespace."""
        result = DiscountCalculator.calculate_discount(5000, " PREMIUM ")
        # This will NOT match due to whitespace, so no discount
        self.assertEqual(result, 5000.0)

    def test_special_characters_in_customer_type(self):
        """Test customer type with special characters."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM!")
        # This will NOT match, so no discount
        self.assertEqual(result, 5000.0)

    def test_numeric_customer_type(self):
        """Test numeric customer type."""
        result = DiscountCalculator.calculate_discount(5000, "123")
        # This will NOT match, so no discount
        self.assertEqual(result, 5000.0)

    def test_return_type(self):
        """Test return type is always float."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        self.assertIsInstance(result, float)

    def test_boundary_conditions(self):
        """Test various boundary conditions."""
        test_cases = [
            (0, "PREMIUM", 0.0),
            (1, "PREMIUM", 0.8),
            (9999, "PREMIUM", 7999.2),
            (10000, "PREMIUM", 8000.0),
            (10001, "PREMIUM", 7500.75),
            (0, "STANDARD", 0.0),
            (10000, "STANDARD", 9000.0),
            (10001, "STANDARD", 8500.85),
        ]
        
        for amount, customer_type, expected in test_cases:
            with self.subTest(amount=amount, customer_type=customer_type):
                result = DiscountCalculator.calculate_discount(amount, customer_type)
                self.assertAlmostEqual(result, expected, places=2)

    def test_consistency(self):
        """Test calculation consistency - same input always produces same output."""
        amount = 7500
        customer_type = "PREMIUM"
        
        results = [DiscountCalculator.calculate_discount(amount, customer_type) 
                   for _ in range(100)]
        
        # All results should be identical
        self.assertTrue(all(r == results[0] for r in results))

    def test_precision(self):
        """Test floating-point precision in calculations."""
        result = DiscountCalculator.calculate_discount(12345.67, "PREMIUM")
        expected = 9876.536  # 12345.67 * 0.80
        self.assertAlmostEqual(result, expected, places=2)


class TestDiscountCalculatorIntegration(unittest.TestCase):
    """Integration tests for DiscountCalculator."""

    def test_realistic_scenario_premium(self):
        """Test realistic premium customer scenario."""
        # Customer buys $8,500 worth of products
        result = DiscountCalculator.calculate_discount(8500, "PREMIUM")
        self.assertEqual(result, 6800.0)
        
        # Verify savings
        savings = 8500 - result
        self.assertEqual(savings, 1700.0)

    def test_realistic_scenario_standard_high_value(self):
        """Test realistic standard customer with high-value purchase."""
        # Customer buys $15,000 worth of products
        result = DiscountCalculator.calculate_discount(15000, "STANDARD")
        self.assertEqual(result, 12750.0)
        
        # Verify savings
        savings = 15000 - result
        self.assertEqual(savings, 2250.0)

    def test_batch_processing(self):
        """Test batch processing of multiple transactions."""
        transactions = [
            (5000, "PREMIUM"),
            (3000, "STANDARD"),
            (15000, "PREMIUM"),
            (2000, "UNKNOWN"),
            (12000, "STANDARD"),
        ]
        
        results = [DiscountCalculator.calculate_discount(amt, ctype) 
                   for amt, ctype in transactions]
        
        expected = [4000.0, 2700.0, 11250.0, 2000.0, 10200.0]
        
        for result, exp in zip(results, expected):
            self.assertAlmostEqual(result, exp, places=2)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
