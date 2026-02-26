from typing import List, Dict

class SalesDataProcessor:

    @staticmethod
    def calculate_revenue(records: List[str]) -> Dict[str, float]:
        revenue_by_region: Dict[str, float] = {}

        for record in records:
            parts = record.split(",")
            region = parts[0]
            price = float(parts[1])
            quantity = int(parts[2])

            total = price * quantity

            if quantity > 100:
                total = total * 0.9

            if region not in revenue_by_region:
                revenue_by_region[region] = total
            else:
                revenue_by_region[region] += total

        return revenue_by_region

    @staticmethod
    def filter_high_revenue_regions(revenue_map: Dict[str, float]) -> List[str]:
        result: List[str] = []

        for region, revenue in revenue_map.items():
            if revenue > 50000:
                result.append(region)

        return result

if __name__ == "__main__":
    data: List[str] = [
        "North,1000,50",
        "South,500,200",
        "East,700,80",
        "North,1200,150"
    ]

    revenue = SalesDataProcessor.calculate_revenue(data)
    high_revenue_regions = SalesDataProcessor.filter_high_revenue_regions(revenue)
    print(high_revenue_regions)
