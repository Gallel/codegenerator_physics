/**
 * Generated Physics-Validated Program: problem_006
 * Automatically generated from Modular DSL.
 */
public class problem_006 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double h = 500000.0; // LengthQuantity
        double R_E = 6370000.0; // LengthQuantity
        double M_E = 5.98e+24; // MassQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double r = compute_orbital_radius(R_E, h);
        double v_orb_sq = compute_orbital_speed_squared(G, M_E, r);
        double v_orb = Math.sqrt(v_orb_sq);
        double T = compute_orbital_period(two, pi, r, v_orb);
        double v_0_sq = compute_launch_speed_squared(two, G, M_E, R_E, r);
        double v_0 = Math.sqrt(v_0_sq);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_006\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_orb\": " + v_orb + ",");
        System.out.println("    \"T\": " + T + ",");
        System.out.println("    \"v_0\": " + v_0 + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute orbital radius from Earth's center as the sum of Earth radius and orbital altitude. */
    public static double compute_orbital_radius(double R_E, double h) {
        double r = R_E + h;
        return r;
    }

    /** Apply circular orbit condition to compute v_orb^2 = G*M_E/r. */
    public static double compute_orbital_speed_squared(double G, double M_E, double r) {
        double GM = G * M_E;
        double v_orb_sq = GM / r;
        return v_orb_sq;
    }

    /** Use uniform circular motion to compute orbital period T = 2*pi*r/v_orb. */
    public static double compute_orbital_period(int two, double pi, double r, double v_orb) {
        double two_pi = two * pi;
        double circumference = two_pi * r;
        double T = circumference / v_orb;
        return T;
    }

    /** Use mechanical energy conservation between Earth's surface and the final circular orbit to compute v_0^2 = 2*G*M_E*(1/R_E - 1/(2*r)). */
    public static double compute_launch_speed_squared(int two, double G, double M_E, double R_E, double r) {
        double GM = G * M_E;
        double two_over_r = two / r;
        double two_over_R_E = two / R_E;
        double bracket_twice = two_over_R_E - two_over_r;
        double v_0_sq = GM * bracket_twice;
        return v_0_sq;
    }

}