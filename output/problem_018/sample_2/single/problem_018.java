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
        double kinetic_energy = compute_kinetic_energy(m, v, two);
        double potential_energy = compute_potential_energy(m, g, h);
        double mechanical_energy = compute_mechanical_energy(kinetic_energy, potential_energy);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_018\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"mechanical_energy\": " + mechanical_energy + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute kinetic energy using K = (1/2) m v^2. */
    public static double compute_kinetic_energy(double m, double v, int two) {
        double v_sq = Math.pow(v, two);
        double m_v_sq = m * v_sq;
        double kinetic_energy = m_v_sq / two;
        return kinetic_energy;
    }

    /** Compute gravitational potential energy using U = m g h relative to sea level. */
    public static double compute_potential_energy(double m, double g, double h) {
        double m_g = m * g;
        double potential_energy = m_g * h;
        return potential_energy;
    }

    /** Compute total mechanical energy as the sum of kinetic and potential energies. */
    public static double compute_mechanical_energy(double kinetic_energy, double potential_energy) {
        double mechanical_energy = kinetic_energy + potential_energy;
        return mechanical_energy;
    }

}