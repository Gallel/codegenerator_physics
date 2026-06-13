/**
 * Generated Physics-Validated Program: problem_026
 * Automatically generated from Modular DSL.
 */
public class problem_026 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m_g = 450.0; // MassQuantity
        double V_L = 0.12; // VolumeQuantity
        double g_to_kg = 1000.0; // DimensionlessQuantity
        double cm3_to_m3_factor = 1e-06; // DimensionlessQuantity
        double V_m3 = 0.00012; // VolumeQuantity

        // --- Main Execution Flow ---
        double rho_g_per_mL = compute_density(m_g, V_L);
        double rho_kg_per_m3 = compute_density(m_g, V_m3);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_026\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"rho_g_per_mL\": " + rho_g_per_mL + ",");
        System.out.println("    \"rho_kg_per_m3\": " + rho_kg_per_m3 + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the density relation rho = m / V. */
    public static double compute_density(double m, double V) {
        double rho = m / V;
        return rho;
    }

}