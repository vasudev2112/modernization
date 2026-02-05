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
            final_amount = 0
        return final_amount

if __name__ == "__main__":
    print(DiscountCalculator.calculate_discount(5000, "PREMIUM"))    # 4000
    print(DiscountCalculator.calculate_discount(15000, "STANDARD"))  # 12750
    print(DiscountCalculator.calculate_discount(2000, "UNKNOWN"))    # 2000
