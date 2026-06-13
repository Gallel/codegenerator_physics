/**
 * Generated Physics-Validated Program: problem_015
 * Automatically generated from Modular DSL.
 */
public class problem_015 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double R = 0.5; // LengthQuantity
        double omega = 1.5707963267948966; // AngularVelocityQuantity
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // AngleQuantity

        // --- Main Execution Flow ---
        double linear_velocity = calc_linear_speed(omega, R);
        double centripetal_acceleration = calc_centripetal_acceleration(omega, R, two);
        double period = calc_period(two, pi, omega);
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
    public static double calc_linear_speed(double omega, double R) {
        double v = omega * R;
        return v;
    }

    /** Compute centripetal acceleration magnitude using a_c = omega^2 * R. */
    public static double calc_centripetal_acceleration(double omega, double R, int two) {
        double omega_sq = Math.pow(omega, two);
        double a_c = omega_sq * R;
        return a_c;
    }

    /** Compute the period of uniform circular motion using T = 2*pi / omega. */
    public static double calc_period(int two, double pi, double omega) {
        double two_pi = two * pi;
        double T = two_pi / omega;
        return T;
    }

    /** Compute frequency from the period using f = 1 / T. */
    public static double calc_frequency(double T) {
        double f = 1.0 / T;
        return f;
    }

}