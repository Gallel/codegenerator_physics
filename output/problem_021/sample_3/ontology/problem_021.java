/**
 * Generated Physics-Validated Program: problem_021
 * Automatically generated from Modular DSL.
 */
public class problem_021 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double P = 1200.0; // PowerQuantity
        double t_min = 9.0; // TimeQuantity
        double sixty = 60.0; // DimensionlessQuantity
        double thousand = 1000.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double t_h = time_minutes_to_hours(t_min, sixty);
        double P_kW = power_watts_to_kilowatts(P, thousand);
        double E_kWh = energy_in_kwh(P_kW, t_h);
        double t_s = time_minutes_to_seconds(t_min, sixty);
        double E_J = energy_in_joules(P, t_s);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_021\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_kWh\": " + E_kWh + ",");
        System.out.println("    \"E_J\": " + E_J + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert operating time from minutes to hours for kilowatt-hour calculation. */
    public static double time_minutes_to_hours(double t_min, double sixty) {
        double t_h = t_min / sixty;
        return t_h;
    }

    /** Convert power from watts to kilowatts for kilowatt-hour calculation. */
    public static double power_watts_to_kilowatts(double P, double thousand) {
        double P_kW = P / thousand;
        return P_kW;
    }

    /** Compute consumed electrical energy in kilowatt-hours using energy equals power times time. */
    public static double energy_in_kwh(double P_kW, double t_h) {
        double E_kWh = P_kW * t_h;
        return E_kWh;
    }

    /** Convert operating time from minutes to seconds for joule calculation. */
    public static double time_minutes_to_seconds(double t_min, double sixty) {
        double t_s = sixty * t_min;
        return t_s;
    }

    /** Compute consumed electrical energy in joules using energy equals power times time with watts as joules per second. */
    public static double energy_in_joules(double P, double t_s) {
        double E_J = P * t_s;
        return E_J;
    }

}