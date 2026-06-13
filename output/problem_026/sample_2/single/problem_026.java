/**
 * Generated Physics-Validated Program: problem_026
 * Automatically generated from Modular DSL.
 */
public class problem_026 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 450.0; // MassQuantity
        double V_cm3 = 120.0; // VolumeQuantity
        double g_per_mL_to_kg_per_m3 = 1000.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double rho_g_mL = compute_density(m, V_cm3);
        double rho_kg_m3 = convert_density_to_si(rho_g_mL, g_per_mL_to_kg_per_m3);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_026\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"rho_g_mL\": " + rho_g_mL + ",");
        System.out.println("    \"rho_kg_m3\": " + rho_kg_m3 + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the density definition rho = m / V. */
    public static double compute_density(double mass, double volume) {
        double rho = mass / volume;
        return rho;
    }

    /** Convert density from g/mL to kg/m^3 using the factor 1000. */
    public static double convert_density_to_si(double rho_g_mL, double factor) {
        double rho_si = rho_g_mL * factor;
        return rho_si;
    }

}