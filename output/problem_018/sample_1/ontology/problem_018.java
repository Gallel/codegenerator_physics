/**
 * Generated Physics-Validated Program: problem_018
 * Automatically generated from Modular DSL.
 */
public class problem_018 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 15000.0; // MassQuantity
        double v = 250.0; // VelocityQuantity
        double h = 10000.0; // AltitudeQuantity
        double g = 9.8; // AccelerationQuantity
        double half = 0.5; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double K = compute_kinetic_energy(m, v, half);
        double U = compute_potential_energy(m, g, h);
        double E_mech = compute_mechanical_energy(K, U);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_018\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_mech\": " + E_mech + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute kinetic energy using K = (1/2) m v^2. */
    public static double compute_kinetic_energy(double m, double v, double half) {
        double v_sq = Math.pow(v, 2.0);
        double m_v_sq = m * v_sq;
        double K = half * m_v_sq;
        return K;
    }

    /** Compute gravitational potential energy relative to sea level using U = m g h. */
    public static double compute_potential_energy(double m, double g, double h) {
        double mg = m * g;
        double U = mg * h;
        return U;
    }

    /** Compute total mechanical energy as the sum of kinetic and gravitational potential energies. */
    public static double compute_mechanical_energy(double K, double U) {
        double E_mech = K + U;
        return E_mech;
    }

}