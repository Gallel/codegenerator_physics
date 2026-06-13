/**
 * Generated Physics-Validated Program: problem_026
 * Automatically generated from Modular DSL.
 */
public class problem_026 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m_g = 450.0; // MassQuantity
        double V_cm3_as_mL = 120.0; // VolumeQuantity
        double V_cm3 = 120.0; // VolumeQuantity
        double grams_per_kilogram = 1000.0; // DimensionlessQuantity
        double cm3_to_m3 = 1e-06; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double rho_g_per_mL = compute_density(m_g, V_cm3_as_mL);
        double m_kg = convert_mass_g_to_kg(m_g, grams_per_kilogram);
        double V_m3 = convert_volume_cm3_to_m3(V_cm3, cm3_to_m3);
        double rho_kg_per_m3 = compute_density(m_kg, V_m3);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_026\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"rho_g_per_mL\": " + rho_g_per_mL + ",");
        System.out.println("    \"rho_kg_per_m3\": " + rho_kg_per_m3 + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the density definition rho = m / V. */
    public static double compute_density(double m, double V) {
        double rho = m / V;
        return rho;
    }

    /** Convert mass from grams to kilograms using m_kg = m_g / 1000. */
    public static double convert_mass_g_to_kg(double m_g, double factor) {
        double m_kg = m_g / factor;
        return m_kg;
    }

    /** Convert volume from cubic centimeters to cubic meters using V_m3 = V_cm3 × 10^-6. */
    public static double convert_volume_cm3_to_m3(double V_cm3, double factor) {
        double V_m3 = V_cm3 * factor;
        return V_m3;
    }

}