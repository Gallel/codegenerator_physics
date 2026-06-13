/**
 * Generated Physics-Validated Program: problem_010
 * Automatically generated from Modular DSL.
 */
public class problem_010 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_0 = 25.0; // VelocityQuantity
        double v_f = 0.0; // VelocityQuantity
        double t = 5.0; // TimeQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double a = compute_acceleration(v_0, v_f, t);
        double delta_x = compute_braking_distance(v_0, v_f, t, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_010\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a\": " + a + ",");
        System.out.println("    \"delta_x\": " + delta_x + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration velocity relation a = (v_f - v_0)/t to obtain the braking acceleration. */
    public static double compute_acceleration(double v_initial, double v_final, double time_interval) {
        double delta_v = v_final - v_initial;
        double a = delta_v / time_interval;
        return a;
    }

    /** Apply the constant-acceleration displacement formula delta_x = ((v_0 + v_f)/2) * t using the average velocity during braking. */
    public static double compute_braking_distance(double v_initial, double v_final, double time_interval, int two_const) {
        double velocity_sum = v_initial + v_final;
        double v_avg = velocity_sum / two_const;
        double delta_x = v_avg * time_interval;
        return delta_x;
    }

}