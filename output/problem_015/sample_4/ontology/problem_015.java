/**
 * Generated Physics-Validated Program: problem_015
 * Automatically generated from Modular DSL.
 */
public class problem_015 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double R = 0.5; // LengthQuantity
        double omega = 1.5707963267948966; // AngularVelocityQuantity
        double two_pi = 6.283185307179586; // AngleQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double linear_velocity = calc_linear_speed(omega, R);
        double centripetal_acceleration = calc_centripetal_acceleration(omega, R, two);
        double period = calc_period(two_pi, omega);
        double frequency = calc_frequency(period);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_015\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"linear_velocity\": " + linear_velocity + ",");
        System.out.println("    \"centripetal_acceleration\": " + centripetal_acceleration + ",");
        System.out.println("    \"period\": " + period + ",");
        System.out.println("    \"frequency\": " + frequency + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute linear speed in uniform circular motion using v = omega * R. */
    public static double calc_linear_speed(double omega_in, double R_in) {
        double v = omega_in * R_in;
        return v;
    }

    /** Compute centripetal acceleration using a_c = omega^2 * R. */
    public static double calc_centripetal_acceleration(double omega_in, double R_in, int two_in) {
        double omega_sq = Math.pow(omega_in, two_in);
        double a_c = omega_sq * R_in;
        return a_c;
    }

    /** Compute the period of circular motion using T = 2*pi / omega. */
    public static double calc_period(double two_pi_in, double omega_in) {
        double T = two_pi_in / omega_in;
        return T;
    }

    /** Compute frequency using f = 1 / T. */
    public static double calc_frequency(double T_in) {
        double f = 1.0 / T_in;
        return f;
    }

}