/**
 * Generated Physics-Validated Program: problem_020
 * Automatically generated from Modular DSL.
 */
public class problem_020 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 0.15; // MassQuantity
        double v_0 = 3.0; // VelocityQuantity
        double h_0 = 8.0; // LengthQuantity
        double g = 9.8; // AccelerationQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double K_0 = compute_initial_kinetic_energy(m, v_0, two);
        double U_0 = compute_initial_potential_energy(m, g, h_0);
        double E_mech = compute_mechanical_energy(K_0, U_0);
        double v_f_sq = compute_final_speed_squared(v_0, g, h_0, two);
        double v_f = Math.sqrt(v_f_sq);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_020\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"E_mech\": " + E_mech + ",");
        System.out.println("    \"v_f\": " + v_f + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute initial kinetic energy using K_0 = (1/2) m v_0^2. */
    public static double compute_initial_kinetic_energy(double m, double v_0, int two) {
        double v0_sq = Math.pow(v_0, two);
        double m_v0_sq = m * v0_sq;
        double K_0 = m_v0_sq / two;
        return K_0;
    }

    /** Compute gravitational potential energy relative to the ground using U_0 = m g h_0. */
    public static double compute_initial_potential_energy(double m, double g, double h_0) {
        double mg = m * g;
        double U_0 = mg * h_0;
        return U_0;
    }

    /** Compute total mechanical energy as the sum of kinetic and potential energies, E_mech = K_0 + U_0. */
    public static double compute_mechanical_energy(double K_0, double U_0) {
        double E_mech = K_0 + U_0;
        return E_mech;
    }

    /** Compute final speed squared from constant-acceleration kinematics, v_f^2 = v_0^2 + 2 g h_0. */
    public static double compute_final_speed_squared(double v_0, double g, double h_0, int two) {
        double v0_sq = Math.pow(v_0, two);
        double two_g = two * g;
        double two_g_h0 = two_g * h_0;
        double v_f_sq = v0_sq + two_g_h0;
        return v_f_sq;
    }

}