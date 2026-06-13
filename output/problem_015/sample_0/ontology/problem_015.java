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
        double one = 1.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v = calc_linear_speed(omega, R);
        double a_c = calc_centripetal_acceleration(omega, R, one);
        double T = calc_period(two_pi, omega);
        double f = calc_frequency(one, T);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_015\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v\": " + v + ",");
        System.out.println("    \"a_c\": " + a_c + ",");
        System.out.println("    \"T\": " + T + ",");
        System.out.println("    \"f\": " + f + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute linear speed in uniform circular motion using v = omega * R. */
    public static double calc_linear_speed(double omega_in, double R_in) {
        double v = omega_in * R_in;
        return v;
    }

    /** Compute centripetal acceleration magnitude using a_c = omega^2 * R. */
    public static double calc_centripetal_acceleration(double omega_in, double R_in, double two) {
        double omega_sq = Math.pow(omega_in, two);
        double a_c = omega_sq * R_in;
        return a_c;
    }

    /** Compute the period of one revolution using T = 2*pi / omega. */
    public static double calc_period(double two_pi_in, double omega_in) {
        double T = two_pi_in / omega_in;
        return T;
    }

    /** Compute frequency using f = 1 / T. */
    public static double calc_frequency(double one_in, double T_in) {
        double f = one_in / T_in;
        return f;
    }

}