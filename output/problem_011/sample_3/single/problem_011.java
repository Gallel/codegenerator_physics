/**
 * Generated Physics-Validated Program: problem_011
 * Automatically generated from Modular DSL.
 */
public class problem_011 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double v_0 = 0.0; // VelocityQuantity
        double v_f = 30.0; // VelocityQuantity
        double t = 10.0; // TimeQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double a = compute_acceleration(v_0, v_f, t);
        double distance = compute_displacement(v_0, t, a, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_011\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a\": " + a + ",");
        System.out.println("    \"distance\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the uniform-acceleration velocity relation a = (v_f - v_0)/t. */
    public static double compute_acceleration(double v_initial, double v_final, double time_interval) {
        double delta_v = v_final - v_initial;
        double a = delta_v / time_interval;
        return a;
    }

    /** Apply uniformly accelerated motion displacement relation delta_x = v_0*t + (1/2)*a*t^2. */
    public static double compute_displacement(double v_initial, double time_interval, double acceleration, int two_const) {
        double v0t = v_initial * time_interval;
        double t_sq = Math.pow(time_interval, two_const);
        double a_t_sq = acceleration * t_sq;
        double half_a_t_sq = a_t_sq / two_const;
        double delta_x = v0t + half_a_t_sq;
        return delta_x;
    }

}