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
        double sixty = 60.0; // DimensionlessQuantity
        double one = 1.0; // DimensionlessQuantity
        double two = 2.0; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double frequency = rpm_to_frequency(rotation_rate_rpm, sixty);
        double period = frequency_to_period(one, frequency);
        double omega = frequency_to_angular_speed(two, pi, frequency);
        double a_edge = centripetal_acceleration(omega, r_edge, two);
        double a_inner = centripetal_acceleration(omega, r_inner, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_016\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"period\": " + period + ",");
        System.out.println("    \"frequency\": " + frequency + ",");
        System.out.println("    \"a_edge\": " + a_edge + ",");
        System.out.println("    \"a_inner\": " + a_inner + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Convert rotation rate from revolutions per minute to frequency in hertz using f = rpm / 60. */
    public static double rpm_to_frequency(double rpm, double sixty) {
        double f_hz = rpm / sixty;
        return f_hz;
    }

    /** Compute the period from frequency using T = 1 / f. */
    public static double frequency_to_period(double one, double f) {
        double period = one / f;
        return period;
    }

    /** Compute angular speed using omega = 2 * pi * f. */
    public static double frequency_to_angular_speed(double two, double pi, double f) {
        double two_pi = two * pi;
        double omega = two_pi * f;
        return omega;
    }

    /** Compute centripetal acceleration magnitude using a_c = omega^2 * r. */
    public static double centripetal_acceleration(double omega, double r, double two) {
        double omega_sq = Math.pow(omega, two);
        double a_c = omega_sq * r;
        return a_c;
    }

}