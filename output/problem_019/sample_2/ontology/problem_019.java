/**
 * Generated Physics-Validated Program: problem_019
 * Automatically generated from Modular DSL.
 */
public class problem_019 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double P = 3000.0; // PowerQuantity
        double t_day = 8.0; // TimeQuantity
        double seconds_per_hour = 3600.0; // DimensionlessQuantity
        int N_days = 30; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double t_day_seconds = convert_hours_to_seconds(t_day, seconds_per_hour);
        double E_day = compute_energy_from_power_time(P, t_day_seconds);
        double E_month = scale_energy_by_days(E_day, N_days);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_019\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_day\": " + E_day + ",");
        System.out.println("    \"E_month\": " + E_month + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert operating time from hours to seconds to keep units consistent with watts and obtain energy in joules. */
    public static double convert_hours_to_seconds(double time_hours, double sec_per_hour) {
        double time_seconds = time_hours * sec_per_hour;
        return time_seconds;
    }

    /** Apply the constant-power energy relation E = P * t. */
    public static double compute_energy_from_power_time(double power, double time) {
        double energy = power * time;
        return energy;
    }

    /** Compute total monthly energy by multiplying daily energy by the number of days. */
    public static double scale_energy_by_days(double daily_energy, int days) {
        double monthly_energy = daily_energy * days;
        return monthly_energy;
    }

}