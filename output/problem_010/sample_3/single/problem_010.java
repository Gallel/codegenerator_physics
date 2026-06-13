/**
 * Generated Physics-Validated Program: problem_010
 * Automatically generated from Modular DSL.
 */
public class problem_010 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v0_kmh = 90.0; // VelocityQuantity
        double conversion_factor = 3.6; // DimensionlessQuantity
        double v_f = 0.0; // VelocityQuantity
        double t = 5.0; // TimeQuantity

        // --- Main Execution Flow ---
        double v_0 = v0_kmh / conversion_factor;
        double two = 0.0;
        double a = compute_acceleration(v_0, v_f, t);
        double delta_x = compute_braking_distance(v_0, v_f, t, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_010\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a\": " + a + ",");
        System.out.println("    \"delta_x\": " + delta_x + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration velocity relation a = (v_f - v_0)/t during braking. */
    public static double compute_acceleration(double v_0, double v_f, double t) {
        double delta_v = v_f - v_0;
        double a = delta_v / t;
        return a;
    }

    /** Apply the uniform-acceleration displacement relation delta_x = ((v_0 + v_f)/2) * t using the average velocity. */
    public static double compute_braking_distance(double v_0, double v_f, double t, double two) {
        double velocity_sum = v_0 + v_f;
        double v_avg = velocity_sum / two;
        double delta_x = v_avg * t;
        return delta_x;
    }

}