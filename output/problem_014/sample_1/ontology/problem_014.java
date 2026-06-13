/**
 * Generated Physics-Validated Program: problem_014
 * Automatically generated from Modular DSL.
 */
public class problem_014 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double r = 0.5; // LengthQuantity
        double f = 10.0; // FrequencyQuantity
        int one = 1; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double T = compute_period(one, f);
        double omega = compute_angular_velocity(two, pi, f);
        double v = compute_linear_speed(omega, r);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_014\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"T\": " + T + ",");
        System.out.println("    \"omega\": " + omega + ",");
        System.out.println("    \"v\": " + v + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Use the reciprocal relation between period and frequency for uniform circular motion: T = 1 / f. */
    public static double compute_period(int one, double f) {
        double T = one / f;
        return T;
    }

    /** Compute angular velocity from frequency using omega = 2*pi*f. */
    public static double compute_angular_velocity(int two, double pi, double f) {
        double two_pi = two * pi;
        double omega = two_pi * f;
        return omega;
    }

    /** Compute the tangential linear speed in uniform circular motion using v = omega*r. */
    public static double compute_linear_speed(double omega, double r) {
        double v = omega * r;
        return v;
    }

}