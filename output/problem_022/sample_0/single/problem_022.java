/**
 * Generated Physics-Validated Program: problem_022
 * Automatically generated from Modular DSL.
 */
public class problem_022 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 1300.0; // MassQuantity
        double v = 30.0; // VelocityQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double kinetic_energy = compute_kinetic_energy(m, v, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_022\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"kinetic_energy\": " + kinetic_energy + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the translational kinetic energy formula KE = (1/2) * m * v^2 by squaring velocity, multiplying by mass, and dividing by 2. */
    public static double compute_kinetic_energy(double m, double v, int two) {
        double v_squared = Math.pow(v, two);
        double m_times_v_squared = m * v_squared;
        double kinetic_energy = m_times_v_squared / two;
        return kinetic_energy;
    }

}