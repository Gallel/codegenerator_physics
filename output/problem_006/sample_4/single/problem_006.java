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
        double v_orb_sq = compute_orbital_speed_radicand(G, M_E, r);
        double v_orb = Math.sqrt(v_orb_sq);
        double T = compute_orbital_period(two, pi, r, v_orb);
        double v0_sq = compute_launch_speed_radicand(two, G, M_E, R_E, r);
        double v_0 = Math.sqrt(v0_sq);
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

    /** Compute the radicand for circular orbital speed using v_orb^2 = G M_E / r. */
    public static double compute_orbital_speed_radicand(double G, double M_E, double r) {
        double GM = G * M_E;
        double v_orb_sq = GM / r;
        return v_orb_sq;
    }

    /** Compute orbital period from uniform circular motion T = 2 pi r / v_orb. */
    public static double compute_orbital_period(int two, double pi, double r, double v_orb) {
        double two_pi = two * pi;
        double circumference = two_pi * r;
        double T = circumference / v_orb;
        return T;
    }

    /** Compute the radicand for the minimum launch speed from Earth's surface using energy conservation v_0^2 = 2 G M_E (1/R_E - 1/(2r)). */
    public static double compute_launch_speed_radicand(int two, double G, double M_E, double R_E, double r) {
        double GM = G * M_E;
        double two_over_R_E = two / R_E;
        double two_over_r = two / r;
        double difference_term = two_over_R_E - two_over_r;
        double v0_sq = GM * difference_term;
        return v0_sq;
    }

}