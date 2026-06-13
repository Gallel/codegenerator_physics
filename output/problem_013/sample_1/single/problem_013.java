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
        double v_f_at_max = 0.0; // VelocityQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double y_max = compute_max_height(v_f_at_max, v_0, a, two, y_0);
        double t_top = compute_time_to_top(v_f_at_max, v_0, a);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_013\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"y_max\": " + y_max + ",");
        System.out.println("    \"t_top\": " + t_top + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation v_f^2 = v_0^2 + 2*a*delta_y and then y_max = y_0 + delta_y to obtain the maximum height. */
    public static double compute_max_height(double v_f, double v_0, double a, int two, double y_0) {
        double v_f_sq = Math.pow(v_f, two);
        double v_0_sq = Math.pow(v_0, two);
        double numerator = v_f_sq - v_0_sq;
        double denominator = two * a;
        double delta_y = numerator / denominator;
        double y_max = y_0 + delta_y;
        return y_max;
    }

    /** Use the linear kinematic relation t = (v_f - v_0)/a to find the time to reach maximum height. */
    public static double compute_time_to_top(double v_f, double v_0, double a) {
        double delta_v = v_f - v_0;
        double t_top = delta_v / a;
        return t_top;
    }

}