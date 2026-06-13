/**
 * Generated Physics-Validated Program: problem_019
 * Automatically generated from Modular DSL.
 */
public class problem_019 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double P = 3000.0; // PowerQuantity
        double t_day_hours = 8.0; // TimeQuantity
        double hours_to_seconds = 3600.0; // DimensionlessQuantity
        int N_days = 30; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double t_day = convert_hours_to_seconds(t_day_hours, hours_to_seconds);
        double E_day = compute_energy_from_power_time(P, t_day);
        double E_month = compute_total_energy_over_days(E_day, N_days);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_019\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_day\": " + E_day + ",");
        System.out.println("    \"E_month\": " + E_month + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert operating time from hours to seconds using the SI conversion factor. */
    public static double convert_hours_to_seconds(double t_hours, double conv) {
        double t_seconds = t_hours * conv;
        return t_seconds;
    }

    /** Apply the power-energy relation E = P * t. */
    public static double compute_energy_from_power_time(double power, double time) {
        double energy = power * time;
        return energy;
    }

    /** Compute total energy over multiple days using E_total = E_day * N_days. */
    public static double compute_total_energy_over_days(double daily_energy, int days) {
        double monthly_energy = daily_energy * days;
        return monthly_energy;
    }

}