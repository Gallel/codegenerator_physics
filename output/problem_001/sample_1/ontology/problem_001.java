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
        int neg_one = -1; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double kinetic_energy = compute_kinetic_energy_circular_orbit(G, M, m, r, two);
        double mechanical_energy = compute_mechanical_energy_from_kinetic(kinetic_energy, neg_one);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_001\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"kinetic_energy\": " + kinetic_energy + ",");
        System.out.println("    \"mechanical_energy\": " + mechanical_energy + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** For a circular orbit, use v^2 = G*M/r from equating gravitational and centripetal forces, then compute kinetic energy K = (1/2) m v^2, giving K = G*M*m/(2*r). */
    public static double compute_kinetic_energy_circular_orbit(double G, double M, double m, double r, int two) {
        double GM = G * M;
        double GMm = GM * m;
        double two_r = two * r;
        double K = GMm / two_r;
        return K;
    }

    /** For a circular gravitational orbit, the total mechanical energy is E_mech = -K. */
    public static double compute_mechanical_energy_from_kinetic(double K, int neg_one) {
        double E_mech = neg_one * K;
        return E_mech;
    }

}