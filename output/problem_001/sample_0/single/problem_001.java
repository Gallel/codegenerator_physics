/**
 * Generated Physics-Validated Program: problem_001
 * Automatically generated from Modular DSL.
 */
public class problem_001 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double r = 9377000.0; // LengthQuantity
        double M = 6.39e+23; // MassQuantity
        double m = 1.08e+16; // MassQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double GMm = compute_gravitational_product(G, M, m);
        double kinetic_energy = compute_kinetic_energy_circular_orbit(GMm, r, two);
        double mechanical_energy = compute_mechanical_energy_circular_orbit(kinetic_energy);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_001\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"kinetic_energy\": " + kinetic_energy + ",");
        System.out.println("    \"mechanical_energy\": " + mechanical_energy + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute the common numerator G*M*m used in circular-orbit kinetic and mechanical energy formulas. */
    public static double compute_gravitational_product(double G, double M, double m) {
        double GM = G * M;
        double GMm = GM * m;
        return GMm;
    }

    /** Apply the circular-orbit result K = G*M*m/(2*r) for orbital kinetic energy. */
    public static double compute_kinetic_energy_circular_orbit(double GMm, double r, int two) {
        double two_r = two * r;
        double K = GMm / two_r;
        return K;
    }

    /** Apply the circular-orbit result E = -G*M*m/(2*r) for total mechanical energy. */
    public static double compute_mechanical_energy_circular_orbit(double K) {
        double E = 0.0 - K;
        return E;
    }

}