/**
 * Generated Physics-Validated Program: problem_016
 * Automatically generated from Modular DSL.
 */
public class problem_016 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double rotation_rate_rpm = 300.0; // DimensionlessQuantity
        double sixty = 60.0; // DimensionlessQuantity
        double one = 1.0; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity
        double r_edge = 0.1; // LengthQuantity
        double r_inner = 0.05; // LengthQuantity

        // --- Main Execution Flow ---
        double frequency = compute_frequency(rotation_rate_rpm, sixty);
        double period = compute_period(one, frequency);
        double omega = compute_angular_speed(two, pi, frequency);
        double a_c_edge = compute_centripetal_acceleration(omega, r_edge, two);
        double a_c_inner = compute_centripetal_acceleration(omega, r_inner, two);
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

    /** Convert rotation rate from revolutions per minute to frequency in hertz using f = rotation_rate_rpm / 60. */
    public static double compute_frequency(double rotation_rate_rpm, double sixty) {
        double frequency_hz = rotation_rate_rpm / sixty;
        return frequency_hz;
    }

    /** Compute period from frequency using T = 1 / f. */
    public static double compute_period(double one, double frequency_hz) {
        double period = one / frequency_hz;
        return period;
    }

    /** Compute angular speed using omega = 2 * pi * f. */
    public static double compute_angular_speed(int two, double pi, double frequency_hz) {
        double two_pi = two * pi;
        double omega = two_pi * frequency_hz;
        return omega;
    }

    /** Compute centripetal acceleration magnitude using a_c = omega^2 * r. */
    public static double compute_centripetal_acceleration(double omega, double r, int two) {
        double omega_squared = Math.pow(omega, two);
        double a_c = omega_squared * r;
        return a_c;
    }

}