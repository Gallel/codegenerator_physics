/**
 * Generated Physics-Validated Program: problem_013
 * Automatically generated from Modular DSL.
 */
public class problem_013 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_0 = 15.0; // VelocityQuantity
        double a = -9.8; // AccelerationQuantity
        double y_0 = 0.0; // LengthQuantity
        double v_top = 0.0; // VelocityQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double delta_y = compute_displacement_to_top(v_top, v_0, a, two);
        double y_top = compute_maximum_height(y_0, delta_y);
        double t_top = compute_time_to_top(v_top, v_0, a);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_013\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"y_top\": " + y_top + ",");
        System.out.println("    \"t_top\": " + t_top + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation v_top^2 = v_0^2 + 2 a Δy and solve algebraically for Δy = (v_top^2 - v_0^2)/(2a). */
    public static double compute_displacement_to_top(double v_top, double v_0, double a, int two) {
        double v_top_sq = Math.pow(v_top, two);
        double v_0_sq = Math.pow(v_0, two);
        double numerator = v_top_sq - v_0_sq;
        double denominator = two * a;
        double delta_y = numerator / denominator;
        return delta_y;
    }

    /** Compute the top position from y_top = y_0 + Δy. */
    public static double compute_maximum_height(double y_0, double delta_y) {
        double y_top = y_0 + delta_y;
        return y_top;
    }

    /** Apply the constant-acceleration velocity relation t_top = (v_top - v_0)/a. */
    public static double compute_time_to_top(double v_top, double v_0, double a) {
        double time_numerator = v_top - v_0;
        double t_top = time_numerator / a;
        return t_top;
    }

}