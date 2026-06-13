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
        double delta_x = compute_braking_distance(v_0, a, t, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_010\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"a\": " + a + ",");
        System.out.println("    \"delta_x\": " + delta_x + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the uniformly accelerated motion velocity relation a = (v_f - v_0)/t to obtain the constant braking acceleration. */
    public static double compute_acceleration(double v_initial, double v_final, double time) {
        double delta_v = v_final - v_initial;
        double a = delta_v / time;
        return a;
    }

    /** Apply the constant-acceleration displacement relation delta_x = v_0 t + (1/2) a t^2 to obtain the distance traveled during braking. */
    public static double compute_braking_distance(double v_initial, double acceleration, double time, int two_const) {
        double t_squared = Math.pow(time, two_const);
        double term1 = v_initial * time;
        double a_t_squared = acceleration * t_squared;
        double term2 = a_t_squared / two_const;
        double delta_x = term1 + term2;
        return delta_x;
    }

}