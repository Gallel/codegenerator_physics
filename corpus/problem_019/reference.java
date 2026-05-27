public class problem_019 {

    public static void main(String[] args) {
        // Energy consumed: E = P * t.
        double power = 3000;
        double hoursPerDay = 8;
        double days = 30;

        double dailyEnergy = power * hoursPerDay * 3600;
        double monthlyEnergy = dailyEnergy * days;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_019\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"daily_energy_consumed\": " + dailyEnergy + ",");
        System.out.println("    \"monthly_energy_consumed\": " + monthlyEnergy + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
