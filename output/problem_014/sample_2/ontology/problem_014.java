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
        double T = compute_period(f, one);
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

    /** Compute the period from frequency using T = 1/f. */
    public static double compute_period(double f_in, int one_in) {
        double T = one_in / f_in;
        return T;
    }

    /** Compute angular velocity for uniform circular motion using omega = 2*pi*f. */
    public static double compute_angular_velocity(int two_in, double pi_in, double f_in) {
        double two_pi = two_in * pi_in;
        double omega = two_pi * f_in;
        return omega;
    }

    /** Compute tangential linear velocity using v = omega*r. */
    public static double compute_linear_velocity(double omega_in, double r_in) {
        double v = omega_in * r_in;
        return v;
    }

}