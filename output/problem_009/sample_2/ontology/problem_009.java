/**
 * Generated Physics-Validated Program: problem_009
 * Automatically generated from Modular DSL.
 */
public class problem_009 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_0 = 22.2222222222; // VelocityQuantity
        double a = -3.0; // AccelerationQuantity
        double t = 6.0; // TimeQuantity
        double half = 0.5; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_f = compute_final_velocity(v_0, a, t);
        double distance = compute_braking_distance(v_0, a, t, half);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_009\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_f\": " + v_f + ",");
        System.out.println("    \"distance\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply constant-acceleration kinematics to compute final velocity: v_f = v_0 + a t. */
    public static double compute_final_velocity(double v_0, double a, double t) {
        double a_t = a * t;
        double v_f = v_0 + a_t;
        return v_f;
    }

    /** Apply constant-acceleration displacement relation for one-dimensional motion: distance = v_0 t + (1/2) a t^2. */
    public static double compute_braking_distance(double v_0, double a, double t, double half) {
        double v0_t = v_0 * t;
        double t_sq = Math.pow(t, 2.0);
        double a_t_sq = a * t_sq;
        double half_a_t_sq = half * a_t_sq;
        double distance = v0_t + half_a_t_sq;
        return distance;
    }

}