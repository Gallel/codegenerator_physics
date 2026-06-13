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
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_final = compute_final_velocity(v_0, a, t);
        double distance = compute_braking_displacement(v_0, a, t, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_009\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_final\": " + v_final + ",");
        System.out.println("    \"distance\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the constant-acceleration velocity relation v = v_0 + a t. */
    public static double compute_final_velocity(double v_0, double a, double t) {
        double a_t = a * t;
        double v = v_0 + a_t;
        return v;
    }

    /** Apply the constant-acceleration displacement relation Δx = v_0 t + (1/2) a t^2. */
    public static double compute_braking_displacement(double v_0, double a, double t, int two) {
        double v0_t = v_0 * t;
        double t_sq = Math.pow(t, two);
        double a_t_sq = a * t_sq;
        double half_a_t_sq = a_t_sq / two;
        double delta_x = v0_t + half_a_t_sq;
        return delta_x;
    }

}