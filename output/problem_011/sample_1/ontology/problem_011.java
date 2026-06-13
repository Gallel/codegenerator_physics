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
        double km_to_m = 1000.0; // DimensionlessQuantity
        double h_to_s = 3600.0; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_f = convert_speed_kmh_to_ms(v_f_kmh, km_to_m, h_to_s);
        double a = compute_acceleration(v_f, v_0, t);
        double distance = compute_distance_from_rest_uarm(v_0, t, a, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_011\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a\": " + a + ",");
        System.out.println("    \"distance\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert speed from kilometers per hour to meters per second using v = v_kmh * 1000 / 3600. */
    public static double convert_speed_kmh_to_ms(double v_kmh, double km_to_m, double h_to_s) {
        double speed_m_per_h = v_kmh * km_to_m;
        double v_ms = speed_m_per_h / h_to_s;
        return v_ms;
    }

    /** Apply uniform acceleration relation a = (v_f - v_0) / t. */
    public static double compute_acceleration(double v_f, double v_0, double t) {
        double delta_v = v_f - v_0;
        double a = delta_v / t;
        return a;
    }

    /** Compute forward distance during uniformly accelerated motion using delta_x = v_0*t + (1/2)*a*t^2. */
    public static double compute_distance_from_rest_uarm(double v_0, double t, double a, int two) {
        double v0t = v_0 * t;
        double t_squared = Math.pow(t, two);
        double a_t_squared = a * t_squared;
        double half_a_t_squared = a_t_squared / two;
        double distance = v0t + half_a_t_squared;
        return distance;
    }

}