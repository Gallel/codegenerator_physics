/**
 * Generated Physics-Validated Program: problem_013
 * Automatically generated from Modular DSL.
 */
public class problem_013 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_0 = 15.0; // VelocityQuantity
        double a = -9.8; // AccelerationQuantity
        double v_top = 0.0; // VelocityQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double max_height = compute_max_height(v_top, v_0, a, two);
        double time_to_top = compute_time_to_top(v_top, v_0, a);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_013\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"max_height\": " + max_height + ",");
        System.out.println("    \"time_to_top\": " + time_to_top + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the kinematic relation v_top^2 = v_0^2 + 2*a*delta_y and solve for the vertical displacement to the top. */
    public static double compute_max_height(double v_top, double v_0, double a, int two) {
        double v_top_sq = Math.pow(v_top, two);
        double v_0_sq = Math.pow(v_0, two);
        double numerator = v_top_sq - v_0_sq;
        double denominator = two * a;
        double delta_y = numerator / denominator;
        return delta_y;
    }

    /** Use the linear kinematic equation v_top = v_0 + a*t and solve for the elapsed time to reach maximum height. */
    public static double compute_time_to_top(double v_top, double v_0, double a) {
        double time_numerator = v_top - v_0;
        double t_top = time_numerator / a;
        return t_top;
    }

}