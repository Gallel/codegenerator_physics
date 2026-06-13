/**
 * Generated Physics-Validated Program: problem_014
 * Automatically generated from Modular DSL.
 */
public class problem_014 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double r = 0.5; // LengthQuantity
        double f = 10.0; // FrequencyQuantity
        double one = 1.0; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double T = compute_period(one, f);
        double omega = compute_angular_velocity(two, pi, f);
        double v = compute_linear_velocity(omega, r);
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

    /** Apply the frequency-period relation for uniform circular motion: T = 1/f. */
    public static double compute_period(double one, double f) {
        double T = one / f;
        return T;
    }

    /** Apply the angular velocity relation for uniform circular motion: omega = 2*pi*f. */
    public static double compute_angular_velocity(int two, double pi, double f) {
        double two_pi = two * pi;
        double omega = two_pi * f;
        return omega;
    }

    /** Apply the tangential speed relation in uniform circular motion: v = omega*r. */
    public static double compute_linear_velocity(double omega, double r) {
        double v = omega * r;
        return v;
    }

}