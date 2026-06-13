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
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double h = compute_free_fall_height(v_f, v_0, g, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_012\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"h\": " + h + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation for free fall from rest, rearranged as h = (v_f^2 - v_0^2)/(2g). */
    public static double compute_free_fall_height(double v_f, double v_0, double g, int two) {
        double v_f_sq = Math.pow(v_f, two);
        double v_0_sq = Math.pow(v_0, two);
        double numerator = v_f_sq - v_0_sq;
        double denominator = two * g;
        double h = numerator / denominator;
        return h;
    }

}