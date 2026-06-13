/**
 * Generated Physics-Validated Program: problem_018
 * Automatically generated from Modular DSL.
 */
public class problem_018 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 15000.0; // MassQuantity
        double v = 250.0; // VelocityQuantity
        double h = 10000.0; // LengthQuantity
        double g = 9.8; // AccelerationQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double ke = compute_kinetic_energy(m, v, two);
        double u = compute_potential_energy(m, g, h);
        double e_mech = compute_mechanical_energy(ke, u);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_018\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"e_mech\": " + e_mech + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Calculate kinetic energy using KE = (1/2) * m * v^2. */
    public static double compute_kinetic_energy(double m, double v, int two) {
        double v_sq = Math.pow(v, two);
        double m_v_sq = m * v_sq;
        double ke = m_v_sq / two;
        return ke;
    }

    /** Calculate gravitational potential energy using U = m * g * h relative to sea level. */
    public static double compute_potential_energy(double m, double g, double h) {
        double mg = m * g;
        double u = mg * h;
        return u;
    }

    /** Calculate total mechanical energy as the sum of kinetic and potential energies. */
    public static double compute_mechanical_energy(double ke, double u) {
        double e_mech = ke + u;
        return e_mech;
    }

}