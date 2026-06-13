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
        double a_avg = compute_average_acceleration(v_i, v_f, delta_t);
        double F_avg = compute_average_force(m, a_avg);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_025\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"F_avg\": " + F_avg + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute average acceleration from change in velocity over the time interval: a_avg = (v_f - v_i) / delta_t. */
    public static double compute_average_acceleration(double v_i, double v_f, double delta_t) {
        double delta_v = v_f - v_i;
        double a_avg = delta_v / delta_t;
        return a_avg;
    }

    /** Apply Newton's second law in average form: F_avg = m * a_avg. */
    public static double compute_average_force(double m, double a_avg) {
        double F_avg = m * a_avg;
        return F_avg;
    }

}