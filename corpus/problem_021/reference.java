public class problem_021 {

    public static void main(String[] args) {
        // Energy consumed by a microwave: E = P * t.
        double power = 1200;
        double minutes = 9;

        double energyJoules = power * minutes * 60;
        double energyKwh = energyJoules / 3.6e6;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_021\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"energy_consumed_kwh\": " + energyKwh + ",");
        System.out.println("    \"energy_consumed_j\": " + energyJoules + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
