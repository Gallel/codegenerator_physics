/**
 * Generated Physics-Validated Program: problem_025
 * Automatically generated from Modular DSL.
 */
public class problem_025 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 0.08; // MassQuantity
        double v_i = 0.0; // VelocityQuantity
        double v_f = 0.6; // VelocityQuantity
        double delta_t = 0.16; // TimeQuantity

        // --- Main Execution Flow ---
        double delta_v = compute_delta_v(v_f, v_i);
        double a_avg = compute_average_acceleration(delta_v, delta_t);
        double F_avg = compute_average_force(m, a_avg);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_025\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"F_avg\": " + F_avg + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute the change in velocity from final and initial velocities. */
    public static double compute_delta_v(double v_f, double v_i) {
        double delta_v = v_f - v_i;
        return delta_v;
    }

    /** Compute average acceleration as change in velocity divided by elapsed time. */
    public static double compute_average_acceleration(double delta_v, double delta_t) {
        double a_avg = delta_v / delta_t;
        return a_avg;
    }

    /** Apply Newton's second law to compute average force from mass and average acceleration. */
    public static double compute_average_force(double m, double a_avg) {
        double F_avg = m * a_avg;
        return F_avg;
    }

}