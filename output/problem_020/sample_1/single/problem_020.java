/**
 * Generated Physics-Validated Program: problem_020
 * Automatically generated from Modular DSL.
 */
public class problem_020 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 0.15; // MassQuantity
        double v_0 = 3.0; // VelocityQuantity
        double y_0 = 8.0; // LengthQuantity
        double y_f = 0.0; // LengthQuantity
        double g = 9.8; // AccelerationQuantity
        double half = 0.5; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity
        int minus_one = -1; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double E_mech = compute_mechanical_energy(m, v_0, g, y_0, half, two);
        double v_f_sq = compute_final_speed_squared(v_0, g, y_0, y_f, two, minus_one);
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

    /** Compute total mechanical energy at the initial height as the sum of kinetic and gravitational potential energies. */
    public static double compute_mechanical_energy(double m, double v_0, double g, double y_0, double half, int two) {
        double v0_sq = Math.pow(v_0, two);
        double half_m = half * m;
        double K_0 = half_m * v0_sq;
        double mg = m * g;
        double U_0 = mg * y_0;
        double E_mech = K_0 + U_0;
        return E_mech;
    }

    /** Use constant-acceleration kinematics with upward positive to compute the final speed squared at the ground. */
    public static double compute_final_speed_squared(double v_0, double g, double y_0, double y_f, int two, int minus_one) {
        double delta_y = y_f - y_0;
        double a = minus_one * g;
        double v0_sq = Math.pow(v_0, two);
        double two_a = two * a;
        double two_a_delta_y = two_a * delta_y;
        double v_f_sq = v0_sq + two_a_delta_y;
        return v_f_sq;
    }

}