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
        double kmh_to_ms = 3.6; // DimensionlessQuantity
        double half = 0.5; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_f = convert_speed_to_si(v_f_kmh, kmh_to_ms);
        double a = compute_acceleration(v_f, v_0, t);
        double distance = compute_distance_from_rest(a, t, half, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_011\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a\": " + a + ",");
        System.out.println("    \"distance\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert speed from km/h to m/s using v = v_kmh / 3.6. */
    public static double convert_speed_to_si(double v_kmh, double factor) {
        double v_si = v_kmh / factor;
        return v_si;
    }

    /** Apply uniform acceleration definition a = (v_f - v_0)/t. */
    public static double compute_acceleration(double v_final, double v_initial, double time) {
        double delta_v = v_final - v_initial;
        double a = delta_v / time;
        return a;
    }

    /** Compute displacement during uniformly accelerated motion from rest using delta_x = (1/2) a t^2. */
    public static double compute_distance_from_rest(double a, double t, double half, int two) {
        double t_squared = Math.pow(t, two);
        double a_t_squared = a * t_squared;
        double distance = half * a_t_squared;
        return distance;
    }

}