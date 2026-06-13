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
        double v_final = compute_final_velocity(v_0, a, t);
        double distance_6s = compute_distance(v_0, a, t, one_half, two);
        double engine_force = compute_engine_force(m, a, g);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_017\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_final\": " + v_final + ",");
        System.out.println("    \"distance_6s\": " + distance_6s + ",");
        System.out.println("    \"engine_force\": " + engine_force + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply constant-acceleration kinematics: v = v_0 + a t. */
    public static double compute_final_velocity(double v_0, double a, double t) {
        double a_t = a * t;
        double v = v_0 + a_t;
        return v;
    }

    /** Apply constant-acceleration displacement relation: distance = v_0 t + (1/2) a t^2. */
    public static double compute_distance(double v_0, double a, double t, double one_half, int two) {
        double v0_t = v_0 * t;
        double t_sq = Math.pow(t, two);
        double a_t_sq = a * t_sq;
        double half_a_t_sq = one_half * a_t_sq;
        double distance = v0_t + half_a_t_sq;
        return distance;
    }

    /** Apply Newton's second law in the vertical direction: F_engine = m(a + g). */
    public static double compute_engine_force(double m, double a, double g) {
        double a_plus_g = a + g;
        double F_engine = m * a_plus_g;
        return F_engine;
    }

}