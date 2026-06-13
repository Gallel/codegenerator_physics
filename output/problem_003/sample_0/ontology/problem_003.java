/**
 * Generated Physics-Validated Program: problem_003
 * Automatically generated from Modular DSL.
 */
public class problem_003 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double r = 384000000.0; // LengthQuantity
        double M_E = 5.972e+24; // MassQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_sq = compute_orbital_speed_squared(G, M_E, r);
        double v = Math.sqrt(v_sq);
        double T = compute_orbital_period(two, pi, r, v);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_003\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v\": " + v + ",");
        System.out.println("    \"T\": " + T + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply circular-orbit force balance to compute v^2 = G*M_E/r before taking the positive square root for orbital speed magnitude. */
    public static double compute_orbital_speed_squared(double G, double M_E, double r) {
        double GM = G * M_E;
        double v_sq = GM / r;
        return v_sq;
    }

    /** Use uniform circular motion for a circular orbit: T = 2*pi*r/v. */
    public static double compute_orbital_period(int two, double pi, double r, double v) {
        double two_pi = two * pi;
        double circumference = two_pi * r;
        double T = circumference / v;
        return T;
    }

}