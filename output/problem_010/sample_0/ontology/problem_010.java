/**
 * Generated Physics-Validated Program: problem_010
 * Automatically generated from Modular DSL.
 */
public class problem_010 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_0 = 25.0; // VelocityQuantity
        double v_f = 0.0; // VelocityQuantity
        double t = 5.0; // TimeQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
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

    /** Apply the constant-acceleration velocity relation a = (v_f - v_0)/t for uniformly accelerated rectilinear motion. */
    public static double compute_acceleration(double v_0, double v_f, double t) {
        double delta_v = v_f - v_0;
        double a = delta_v / t;
        return a;
    }

    /** Compute braking distance from average velocity times time: delta_x = ((v_0 + v_f)/2) * t. */
    public static double compute_braking_distance(double v_0, double v_f, double t, int two) {
        double v_sum = v_0 + v_f;
        double v_avg = v_sum / two;
        double delta_x = v_avg * t;
        return delta_x;
    }

}