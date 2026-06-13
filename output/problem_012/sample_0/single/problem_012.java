/**
 * Generated Physics-Validated Program: problem_012
 * Automatically generated from Modular DSL.
 */
public class problem_012 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_f = 15.0; // VelocityQuantity
        double v_0 = 0.0; // VelocityQuantity
        double g = 9.8; // AccelerationQuantity

        // --- Main Execution Flow ---
        double height = compute_free_fall_height(v_f, v_0, g);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_012\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"height\": " + height + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation solved for vertical displacement: delta_y = (v_f^2 - v_0^2)/(2*a), with downward chosen as positive so the displacement equals the falling height. */
    public static double compute_free_fall_height(double v_f, double v_0, double g) {
        double v_f_sq = v_f * v_f;
        double v_0_sq = v_0 * v_0;
        double numerator = v_f_sq - v_0_sq;
        double two_g = g + g;
        double height = numerator / two_g;
        return height;
    }

}