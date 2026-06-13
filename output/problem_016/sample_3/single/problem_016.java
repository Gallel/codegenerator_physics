/**
 * Generated Physics-Validated Program: problem_016
 * Automatically generated from Modular DSL.
 */
public class problem_016 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double r_edge = 0.1; // LengthQuantity
        double r_inner = 0.05; // LengthQuantity
        double rotation_rate_rpm = 300.0; // FrequencyQuantity
        int sixty = 60; // DimensionlessQuantity
        int one = 1; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double frequency = rpm_to_frequency(rotation_rate_rpm, sixty);
        double period = frequency_to_period(one, frequency);
        double omega = compute_angular_speed(two, pi, frequency);
        double a_c_edge = centripetal_acceleration(omega, r_edge, two);
        double a_c_inner = centripetal_acceleration(omega, r_inner, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_016\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"period\": " + period + ",");
        System.out.println("    \"frequency\": " + frequency + ",");
        System.out.println("    \"a_c_edge\": " + a_c_edge + ",");
        System.out.println("    \"a_c_inner\": " + a_c_inner + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert rotation rate from revolutions per minute to frequency in hertz using f = rpm / 60. */
    public static double rpm_to_frequency(double rpm, int sixty) {
        double frequency_hz = rpm / sixty;
        return frequency_hz;
    }

    /** Compute the period from the frequency using T = 1 / f. */
    public static double frequency_to_period(int one, double frequency) {
        double period = one / frequency;
        return period;
    }

    /** Compute angular speed from frequency using omega = 2*pi*f. */
    public static double compute_angular_speed(int two, double pi, double frequency) {
        double two_pi = two * pi;
        double omega = two_pi * frequency;
        return omega;
    }

    /** Compute centripetal acceleration magnitude using a_c = omega^2 * r. */
    public static double centripetal_acceleration(double omega, double r, int two) {
        double omega_sq = Math.pow(omega, two);
        double a_c = omega_sq * r;
        return a_c;
    }

}