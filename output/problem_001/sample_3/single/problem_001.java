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
        double GMm = compute_gravitational_numerator(G, M_mars, m_phobos);
        double K = compute_kinetic_energy_circular_orbit(GMm, r, two);
        double U = compute_potential_energy(GMm, r);
        double E_mech = compute_mechanical_energy(K, U);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_001\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"K\": " + K + ",");
        System.out.println("    \"E_mech\": " + E_mech + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute the common numerator G*M_mars*m_phobos used in circular-orbit kinetic and gravitational potential energy formulas. */
    public static double compute_gravitational_numerator(double G, double M_mars, double m_phobos) {
        double GM = G * M_mars;
        double GMm = GM * m_phobos;
        return GMm;
    }

    /** Apply K = G*M_mars*m_phobos/(2*r) for a circular gravitational orbit. */
    public static double compute_kinetic_energy_circular_orbit(double GMm, double r, int two) {
        double two_r = two * r;
        double K = GMm / two_r;
        return K;
    }

    /** Apply gravitational potential energy U = -G*M_mars*m_phobos/r with zero at infinity. */
    public static double compute_potential_energy(double GMm, double r) {
        double GMm_over_r = GMm / r;
        double zero = GMm_over_r - GMm_over_r;
        double U = zero - GMm_over_r;
        return U;
    }

    /** Apply total mechanical energy E_mech = K + U. */
    public static double compute_mechanical_energy(double K, double U) {
        double E_mech = K + U;
        return E_mech;
    }

}