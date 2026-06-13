/**
 * Generated Physics-Validated Program: problem_001
 * Automatically generated from Modular DSL.
 */
public class problem_001 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double r = 9377000.0; // LengthQuantity
        double M_mars = 6.39e+23; // MassQuantity
        double m_phobos = 1.08e+16; // MassQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double energy_factor = compute_orbital_energy_factor(G, M_mars, m_phobos, r);
        double K = compute_kinetic_energy(energy_factor, two);
        double E_mech = compute_mechanical_energy(K);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_001\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"K\": " + K + ",");
        System.out.println("    \"E_mech\": " + E_mech + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute the common gravitational orbital energy factor G*M_mars*m_phobos/r for a circular orbit. */
    public static double compute_orbital_energy_factor(double G, double M_mars, double m_phobos, double r) {
        double GM = G * M_mars;
        double GMm = GM * m_phobos;
        double energy_factor = GMm / r;
        return energy_factor;
    }

    /** Apply the circular-orbit result K = (G*M_mars*m_phobos)/(2*r). */
    public static double compute_kinetic_energy(double energy_factor, int two) {
        double K = energy_factor / two;
        return K;
    }

    /** Apply the circular-orbit result E_mech = -(G*M_mars*m_phobos)/(2*r) for a bound orbit. */
    public static double compute_mechanical_energy(double K) {
        double E_mech = 0.0 - K;
        return E_mech;
    }

}