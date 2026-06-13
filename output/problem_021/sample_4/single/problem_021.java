/**
 * Generated Physics-Validated Program: problem_021
 * Automatically generated from Modular DSL.
 */
public class problem_021 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double P = 1200.0; // PowerQuantity
        double t_min = 9.0; // TimeQuantity
        double c_60 = 60.0; // DimensionlessQuantity
        double c_1000 = 1000.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double t_h = convert_time_to_hours(t_min, c_60);
        double P_kW = convert_power_to_kilowatts(P, c_1000);
        double E_kWh = compute_energy_kwh(P_kW, t_h);
        double t_s = convert_time_to_seconds(t_min, c_60);
        double E_J = compute_energy_joules(P, t_s);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_021\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_kWh\": " + E_kWh + ",");
        System.out.println("    \"E_J\": " + E_J + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert operating time from minutes to hours using t_h = t_min / 60. */
    public static double convert_time_to_hours(double t_min, double c_60) {
        double t_h = t_min / c_60;
        return t_h;
    }

    /** Convert power from watts to kilowatts using P_kW = P / 1000. */
    public static double convert_power_to_kilowatts(double P, double c_1000) {
        double P_kW = P / c_1000;
        return P_kW;
    }

    /** Calculate electrical energy in kilowatt-hours using E_kWh = P_kW * t_h. */
    public static double compute_energy_kwh(double P_kW, double t_h) {
        double E_kWh = P_kW * t_h;
        return E_kWh;
    }

    /** Convert operating time from minutes to seconds using t_s = 60 * t_min. */
    public static double convert_time_to_seconds(double t_min, double c_60) {
        double t_s = c_60 * t_min;
        return t_s;
    }

    /** Calculate electrical energy in joules using E_J = P * t_s. */
    public static double compute_energy_joules(double P, double t_s) {
        double E_J = P * t_s;
        return E_J;
    }

}