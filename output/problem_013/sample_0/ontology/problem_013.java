/**
 * Generated Physics-Validated Program: problem_013
 * Automatically generated from Modular DSL.
 */
public class problem_013 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_0 = 15.0; // VelocityQuantity
        double a = -9.8; // AccelerationQuantity
        double v_at_max = 0.0; // VelocityQuantity
        int const_2 = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double max_height = compute_max_height(v_at_max, v_0, a, const_2);
        double time_to_max_height = compute_time_to_top(v_at_max, v_0, a);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_013\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"max_height\": " + max_height + ",");
        System.out.println("    \"time_to_max_height\": " + time_to_max_height + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation v_f^2 = v_0^2 + 2 a delta_y and isolate delta_y = (v_f^2 - v_0^2)/(2a) to obtain the maximum height relative to the launch point. */
    public static double compute_max_height(double v_f, double v_i, double a_val, int two) {
        double v_f_sq = Math.pow(v_f, two);
        double v_i_sq = Math.pow(v_i, two);
        double numerator = v_f_sq - v_i_sq;
        double denominator = two * a_val;
        double delta_y = numerator / denominator;
        return delta_y;
    }

    /** Apply the linear kinematic relation t = (v_f - v_0)/a for the ascent to maximum height. */
    public static double compute_time_to_top(double v_f, double v_i, double a_val) {
        double delta_v = v_f - v_i;
        double t_top = delta_v / a_val;
        return t_top;
    }

}