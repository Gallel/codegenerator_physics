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
        int one = 1; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v = compute_linear_speed(omega, R);
        double a_c = compute_centripetal_acceleration(omega, R, two);
        double T = compute_period(two, pi, omega);
        double f = compute_frequency(one, T);
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

    /** Uniform circular motion relation for linear speed: v = omega * R. */
    public static double compute_linear_speed(double omega, double R) {
        double v = omega * R;
        return v;
    }

    /** Centripetal acceleration magnitude in uniform circular motion: a_c = omega^2 * R. */
    public static double compute_centripetal_acceleration(double omega, double R, int two) {
        double omega_sq = Math.pow(omega, two);
        double a_c = omega_sq * R;
        return a_c;
    }

    /** Period of one full revolution from angular velocity: T = 2*pi / omega. */
    public static double compute_period(int two, double pi, double omega) {
        double two_pi = two * pi;
        double T = two_pi / omega;
        return T;
    }

    /** Frequency from period: f = 1 / T. */
    public static double compute_frequency(int one, double T) {
        double f = one / T;
        return f;
    }

}