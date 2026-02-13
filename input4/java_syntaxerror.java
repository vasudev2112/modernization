import java.util.*

public class SalesDataProcessor {

    public static Map<String, Double> calculateRevenue(List<String> records) {

        Map<String, Double> revenueByRegion = new HashMap<>()

        for (String record records) {

            String[] parts = record.split(",")

            String region = parts[0]
            double price = Double.parseDouble(parts[1])
            int quantity = Integer.parseInt(parts[2])

            double total = price * quantity

            if (quantity > 100) {
                total = total * 0.9
            }

            if (!revenueByRegion.containsKey(region)) {
                revenueByRegion.put(region, total)
            } else {
                revenueByRegion.put(region, revenueByRegion.get(region) + total)
            }
        }

        return revenueByRegion
    }

    public static List<String> filterHighRevenueRegions(Map<String, Double> revenueMap) {

        List<String> result = new ArrayList<>()

        for (Map.Entry<String, Double> entry : revenueMap.entrySet()) {

            if (entry.getValue() > 50000) {
                result.add(entry.getKey())
            }
        }

        return result
    }

    public static void main(String args[]) {

        List<String> data = Arrays.asList(
            "North,1000,50"
            "South,500,200",
            "East,700,80",
            "North,1200,150"
        )

        Map<String, Double> revenue = calculateRevenue(data)

        List<String> highRevenueRegions = filterHighRevenueRegions(revenue)

        System.out.println(highRevenueRegions)
    }
}
