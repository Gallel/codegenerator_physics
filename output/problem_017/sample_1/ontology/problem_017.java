/**
 * Generated Physics-Validated Program: problem_017
 * Automatically generated from Modular DSL.
 */
public class problem_017 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 40.0; // MassQuantity
        double t = 6.0; // TimeQuantity
        double a = 15.0; // AccelerationQuantity
        double g = 9.8; // AccelerationQuantity
        double v0 = 0.0; // VelocityQuantity
        double one_half = 0.5; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_6s = compute_final_velocity(v0, a, t);
        double distance_6s = compute_displacement(v0, a, t, one_half, two);
        double engine_thrust = compute_engine_thrust(m, a, g);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_017\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_6s\": " + v_6s + ",");
        System.out.println("    \"distance_6s\": " + distance_6s + ",");
        System.out.println("    \"engine_thrust\": " + engine_thrust + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply constant-acceleration kinematics: v = v0 + a t. */
    public static double compute_final_velocity(double v0, double a, double t) {
        double at = a * t;
        double v = v0 + at;
        return v;
    }

    /** Apply constant-acceleration displacement relation: delta_y = v0 t + (1/2) a t^2. */
    public static double compute_displacement(double v0, double a, double t, double one_half, int two) {
        double v0t = v0 * t;
        double t_sq = Math.pow(t, two);
        double a_t_sq = a * t_sq;
        double half_a_t_sq = one_half * a_t_sq;
        double delta_y = v0t + half_a_t_sq;
        return delta_y;
    }

    /** Apply Newton's second law during ascent: F_engine - mg = ma, so F_engine = m(a + g). */
    public static double compute_engine_thrust(double m, double a, double g) {
        double a_plus_g = a + g;
        double F_engine = m * a_plus_g;
        return F_engine;
    }

}