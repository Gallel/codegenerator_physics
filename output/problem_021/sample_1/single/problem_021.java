/**
 * Generated Physics-Validated Program: problem_021
 * Automatically generated from Modular DSL.
 */
public class problem_021 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double P = 1200.0; // PowerQuantity
        double t_min = 9.0; // TimeQuantity
        double one_thousand = 1000.0; // DimensionlessQuantity
        double sixty = 60.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double P_kW = power_to_kilowatts(P, one_thousand);
        double t_h = minutes_to_hours(t_min, sixty);
        double E_kWh = energy_from_power_time(P_kW, t_h);
        double t_s = minutes_to_seconds(sixty, t_min);
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
    public static double power_to_kilowatts(double P_w, double factor_1000) {
        double P_kW = P_w / factor_1000;
        return P_kW;
    }

    /** Convert time from minutes to hours using t_h = t_min / 60. */
    public static double minutes_to_hours(double t_m, double factor_60) {
        double t_h = t_m / factor_60;
        return t_h;
    }

    /** Compute energy from constant power and elapsed time using E = P * t. */
    public static double energy_from_power_time(double power, double time) {
        double E = power * time;
        return E;
    }

    /** Convert time from minutes to seconds using t_s = 60 * t_min. */
    public static double minutes_to_seconds(double factor_60, double t_m) {
        double t_s = factor_60 * t_m;
        return t_s;
    }

}