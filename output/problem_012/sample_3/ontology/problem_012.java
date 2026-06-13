/**
 * Generated Physics-Validated Program: problem_012
 * Automatically generated from Modular DSL.
 */
public class problem_012 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_f = 15.0; // VelocityQuantity
        double g = 9.8; // AccelerationQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double h = compute_free_fall_height(v_f, g, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_012\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"h\": " + h + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation for free fall from rest, v_f^2 = 2gh, and solve for the positive height h = v_f^2/(2g). */
    public static double compute_free_fall_height(double v_f, double g, int two) {
        double v_f_sq = Math.pow(v_f, two);
        double two_g = two * g;
        double h = v_f_sq / two_g;
        return h;
    }

}