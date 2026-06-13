/**
 * Generated Physics-Validated Program: problem_008
 * Automatically generated from Modular DSL.
 */
public class problem_008 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        int t1_start = 0; // TimeQuantity
        int t1_end = 2; // TimeQuantity
        int v1_start = 2; // VelocityQuantity
        int v1_end = 8; // VelocityQuantity
        int t2_start = 2; // TimeQuantity
        int t2_end = 4; // TimeQuantity
        int v2_constant = 8; // VelocityQuantity
        int t3_start = 4; // TimeQuantity
        int t3_end = 6; // TimeQuantity
        int v3_start = 8; // VelocityQuantity
        int v3_end = 4; // VelocityQuantity

        // --- Main Execution Flow ---
        double delta_t1 = compute_delta_t(t1_start, t1_end);
        double a_avg1 = compute_average_acceleration(v1_start, v1_end, delta_t1);
        double delta_t2 = compute_delta_t(t2_start, t2_end);
        double a_avg2 = compute_average_acceleration(v2_constant, v2_constant, delta_t2);
        double delta_t3 = compute_delta_t(t3_start, t3_end);
        double a_avg3 = compute_average_acceleration(v3_start, v3_end, delta_t3);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_008\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a_avg1\": " + a_avg1 + ",");
        System.out.println("    \"a_avg2\": " + a_avg2 + ",");
        System.out.println("    \"a_avg3\": " + a_avg3 + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute the duration of a segment as end time minus start time. */
    public static double compute_delta_t(double t_start, double t_end) {
        double delta_t = t_end - t_start;
        return delta_t;
    }

    /** Compute average acceleration as velocity change divided by elapsed time. */
    public static double compute_average_acceleration(double v_start, double v_end, double delta_t) {
        double delta_v = v_end - v_start;
        double a_avg = delta_v / delta_t;
        return a_avg;
    }

}