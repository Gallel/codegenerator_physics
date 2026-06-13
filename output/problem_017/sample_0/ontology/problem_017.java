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
        double v_0 = 0.0; // VelocityQuantity
        double one_half = 0.5; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v = compute_velocity_constant_acceleration(v_0, a, t);
        double distance = compute_upward_displacement(v_0, t, a, one_half, two);
        double F_engine = compute_engine_force(m, a, g);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_017\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v\": " + v + ",");
        System.out.println("    \"distance\": " + distance + ",");
        System.out.println("    \"F_engine\": " + F_engine + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation v = v_0 + a t for upward motion. */
    public static double compute_velocity_constant_acceleration(double v_0, double a, double t) {
        double a_t = a * t;
        double v = v_0 + a_t;
        return v;
    }

    /** Apply the constant-acceleration displacement relation delta_x = v_0 t + (1/2) a t^2. */
    public static double compute_upward_displacement(double v_0, double t, double a, double one_half, int two) {
        double v0_t = v_0 * t;
        double t_squared = Math.pow(t, two);
        double a_t_squared = a * t_squared;
        double half_a_t_squared = one_half * a_t_squared;
        double distance = v0_t + half_a_t_squared;
        return distance;
    }

    /** Apply Newton's second law with upward positive: F_engine - mg = ma, so F_engine = m(a + g). */
    public static double compute_engine_force(double m, double a, double g) {
        double a_plus_g = a + g;
        double F_engine = m * a_plus_g;
        return F_engine;
    }

}