/**
 * Generated Physics-Validated Program: problem_021
 * Automatically generated from Modular DSL.
 */
public class problem_021 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double P = 1200.0; // PowerQuantity
        double t_min = 9.0; // TimeQuantity
        double c_1000 = 1000.0; // DimensionlessQuantity
        double c_60 = 60.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double P_kW = power_to_kw(P, c_1000);
        double t_h = minutes_to_hours(t_min, c_60);
        double E_kWh = energy_from_power_time(P_kW, t_h);
        double t_s = minutes_to_seconds(t_min, c_60);
        double E_J = energy_from_power_time(P, t_s);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_021\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_kWh\": " + E_kWh + ",");
        System.out.println("    \"E_J\": " + E_J + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert power from watts to kilowatts using P_kW = P / 1000. */
    public static double power_to_kw(double P_in, double factor_1000) {
        double P_kW = P_in / factor_1000;
        return P_kW;
    }

    /** Convert time from minutes to hours using t_h = t_min / 60. */
    public static double minutes_to_hours(double t_min_in, double factor_60) {
        double t_h = t_min_in / factor_60;
        return t_h;
    }

    /** Compute energy from constant power and time using E = P * t. */
    public static double energy_from_power_time(double power_in, double time_in) {
        double E = power_in * time_in;
        return E;
    }

    /** Convert time from minutes to seconds using t_s = t_min * 60. */
    public static double minutes_to_seconds(double t_min_in, double factor_60) {
        double t_s = t_min_in * factor_60;
        return t_s;
    }

}