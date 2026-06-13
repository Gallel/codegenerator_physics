/**
 * Generated Physics-Validated Program: problem_027
 * Automatically generated from Modular DSL.
 */
public class problem_027 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double S2 = 250.0; // AreaQuantity
        double S1 = 10.0; // AreaQuantity
        double F2 = 12000.0; // ForceQuantity

        // --- Main Execution Flow ---
        double F1 = compute_small_piston_force(F2, S1, S2);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_027\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"F1\": " + F1 + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply Pascal's law with equal pressure in both pistons: F1/S1 = F2/S2, rearranged as F1 = F2 * (S1 / S2). */
    public static double compute_small_piston_force(double F2, double S1, double S2) {
        double area_ratio = S1 / S2;
        double F1 = F2 * area_ratio;
        return F1;
    }

}