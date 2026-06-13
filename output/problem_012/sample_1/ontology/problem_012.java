/**
 * Generated Physics-Validated Program: problem_012
 * Automatically generated from Modular DSL.
 */
public class problem_012 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_ground = 15.0; // VelocityQuantity
        double g = 9.8; // AccelerationQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double h = compute_free_fall_height(v_ground, g, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_012\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"h\": " + h + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation for free fall from rest, rearranged as h = v_f^2 / (2 g). */
    public static double compute_free_fall_height(double v_f, double g_acc, int two_const) {
        double v_f_squared = Math.pow(v_f, two_const);
        double two_g = two_const * g_acc;
        double h = v_f_squared / two_g;
        return h;
    }

}