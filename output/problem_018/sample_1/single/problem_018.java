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
        double sea_level = 0.0; // AltitudeQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double kinetic_energy = compute_kinetic_energy(m, v, two);
        double potential_energy = compute_potential_energy(m, g, h, sea_level);
        double mechanical_energy = kinetic_energy + potential_energy;
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

    /** Compute gravitational potential energy relative to sea level using U = m g (h - 0). */
    public static double compute_potential_energy(double m, double g, double h, double sea_level) {
        double delta_position = h - sea_level;
        double mg = m * g;
        double potential_energy = mg * delta_position;
        return potential_energy;
    }

}