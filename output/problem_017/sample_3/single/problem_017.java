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
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v = compute_velocity_constant_acceleration(v_0, a, t);
        double distance = compute_upward_displacement(v_0, a, t, two);
        double engine_force = compute_engine_thrust(m, a, g);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_017\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v\": " + v + ",");
        System.out.println("    \"distance\": " + distance + ",");
        System.out.println("    \"engine_force\": " + engine_force + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration relation v = v_0 + a t for upward motion. */
    public static double compute_velocity_constant_acceleration(double v_0, double a, double t) {
        double at = a * t;
        double v = v_0 + at;
        return v;
    }

    /** Apply the constant-acceleration displacement relation delta_y = v_0 t + (1/2) a t^2. */
    public static double compute_upward_displacement(double v_0, double a, double t, int two) {
        double v0t = v_0 * t;
        double t_sq = Math.pow(t, two);
        double a_t_sq = a * t_sq;
        double half_a_t_sq = a_t_sq / two;
        double distance = v0t + half_a_t_sq;
        return distance;
    }

    /** Apply Newton's second law vertically: F_engine - m g = m a, so F_engine = m(a + g). */
    public static double compute_engine_thrust(double m, double a, double g) {
        double a_plus_g = a + g;
        double engine_force = m * a_plus_g;
        return engine_force;
    }

}