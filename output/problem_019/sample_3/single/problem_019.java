/**
 * Generated Physics-Validated Program: problem_019
 * Automatically generated from Modular DSL.
 */
public class problem_019 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double P = 3000.0; // PowerQuantity
        double t_day = 8.0; // TimeQuantity
        double N_days = 30.0; // DimensionlessQuantity
        double seconds_per_hour = 3600.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double t_day_s = convert_hours_to_seconds(t_day, seconds_per_hour);
        double E_day = compute_energy_from_power_and_time(P, t_day_s);
        double E_month = scale_by_number_of_days(E_day, N_days);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_019\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_day\": " + E_day + ",");
        System.out.println("    \"E_month\": " + E_month + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert operating time from hours to seconds for SI energy calculation. */
    public static double convert_hours_to_seconds(double time_h, double sec_per_h) {
        double time_s = time_h * sec_per_h;
        return time_s;
    }

    /** Apply the power-energy relation E = P * t. */
    public static double compute_energy_from_power_and_time(double power, double time) {
        double energy = power * time;
        return energy;
    }

    /** Multiply daily energy by the number of days to obtain monthly energy consumption. */
    public static double scale_by_number_of_days(double daily_energy, double days) {
        double total_energy = daily_energy * days;
        return total_energy;
    }

}