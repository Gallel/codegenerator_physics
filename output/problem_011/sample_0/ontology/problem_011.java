/**
 * Generated Physics-Validated Program: problem_011
 * Automatically generated from Modular DSL.
 */
public class problem_011 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_0 = 0.0; // VelocityQuantity
        double v_f_kmh = 108.0; // VelocityQuantity
        double t = 10.0; // TimeQuantity
        double conversion_factor = 3.6; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_f = convert_speed_to_si(v_f_kmh, conversion_factor);
        double a = compute_acceleration(v_f, v_0, t);
        double delta_x = compute_displacement_from_acceleration(a, t, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_011\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a\": " + a + ",");
        System.out.println("    \"delta_x\": " + delta_x + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert final speed from km/h to m/s using division by 3.6. */
    public static double convert_speed_to_si(double v_kmh, double factor) {
        double v_ms = v_kmh / factor;
        return v_ms;
    }

    /** Apply uniformly accelerated motion relation a = (v_f - v_0) / t. */
    public static double compute_acceleration(double v_f, double v_0, double t) {
        double delta_v = v_f - v_0;
        double a = delta_v / t;
        return a;
    }

    /** Apply uniformly accelerated motion displacement formula simplified for v_0 = 0: delta_x = (1/2) a t^2. */
    public static double compute_displacement_from_acceleration(double a, double t, int two) {
        double t_squared = Math.pow(t, two);
        double a_t_squared = a * t_squared;
        double delta_x = a_t_squared / two;
        return delta_x;
    }

}