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
        double v_f = v_f_kmh / conversion_factor;
        double a = compute_acceleration(v_f, v_0, t);
        double distance = compute_displacement_avg_velocity(v_0, v_f, t, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_011\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a\": " + a + ",");
        System.out.println("    \"distance\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply uniform acceleration definition a = (v_f - v_0) / t. */
    public static double compute_acceleration(double v_f, double v_0, double t) {
        double delta_v = v_f - v_0;
        double a = delta_v / t;
        return a;
    }

    /** Use average velocity for uniformly accelerated rectilinear motion: Δx = ((v_0 + v_f) / 2) * t. */
    public static double compute_displacement_avg_velocity(double v_0, double v_f, double t, int two) {
        double v_sum = v_0 + v_f;
        double v_avg = v_sum / two;
        double distance = v_avg * t;
        return distance;
    }

}