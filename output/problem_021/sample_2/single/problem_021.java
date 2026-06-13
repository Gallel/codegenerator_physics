/**
 * Generated Physics-Validated Program: problem_021
 * Automatically generated from Modular DSL.
 */
public class problem_021 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double P = 1200.0; // PowerQuantity
        double t_min = 9.0; // TimeQuantity
        double thousand = 1000.0; // DimensionlessQuantity
        double sixty = 60.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double P_kW = P / thousand;
        double t_h = t_min / sixty;
        double E_kWh = power_time_energy(P_kW, t_h);
        double t_s = sixty * t_min;
        double E_J = power_time_energy(P, t_s);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_021\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_kWh\": " + E_kWh + ",");
        System.out.println("    \"E_J\": " + E_J + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute consumed energy as power multiplied by time after the required unit conversions are performed externally. */
    public static double power_time_energy(double power_value, double time_value) {
        double energy_value = power_value * time_value;
        return energy_value;
    }

}