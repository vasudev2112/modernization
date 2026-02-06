# Converted from Java DiscountCalculator

def calculate_discount(amount, customer_type):
    """
    Calculates the final amount after applying discounts

    :param amount: original purchase amount
    :param customer_type: type of customer (PREMIUM or STANDARD)
    :return: final amount after discount
    """
    discount = 0.0

    # Customer-based discount
    if customer_type.strip().upper() == "PREMIUM":
        discount = 0.20
    elif customer_type.strip().upper() == "STANDARD":
        discount = 0.10

    # High-value purchase additional discount
    if amount > 10000:
        discount += 0.05

    final_amount = amount - (amount * discount)

    # Final amount should never be negative
    if final_amount < 0:
        final_amount = 0

    return final_amount

if __name__ == "__main__":
    print(calculate_discount(5000, "PREMIUM"))    # 4000.0
    print(calculate_discount(15000, "STANDARD"))  # 12750.0
    print(calculate_discount(2000, "UNKNOWN"))    # 2000.0
