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

        // --- Main Execution Flow ---
        double r = compute_orbital_radius(R_E, h);
        double mu = compute_mu(G, M_E);
        double v_orb = compute_orbital_speed(mu, r);
        double T = compute_orbital_period(r, v_orb, two);
        double v_0 = compute_launch_speed(v_orb, mu, R_E, r, two);
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

    /** Compute the standard gravitational parameter mu = G*M_E. */
    public static double compute_mu(double G, double M_E) {
        double mu = G * M_E;
        return mu;
    }

    /** Compute circular orbital speed from v_orb = sqrt(mu/r), returning the positive speed magnitude. */
    public static double compute_orbital_speed(double mu, double r) {
        double mu_over_r = mu / r;
        double v_orb = Math.sqrt(mu_over_r);
        return v_orb;
    }

    /** Compute orbital period for uniform circular motion using T = 2*r/v_orb. */
    public static double compute_orbital_period(double r, double v_orb, int two) {
        double two_r = two * r;
        double T = two_r / v_orb;
        return T;
    }

    /** Apply conservation of mechanical energy to compute launch speed from Earth's surface: v0 = sqrt(v_orb^2 + 2*mu*(1/R_E - 1/r)), returning the positive speed magnitude. */
    public static double compute_launch_speed(double v_orb, double mu, double R_E, double r, int two) {
        double v_orb_sq = Math.pow(v_orb, two);
        double mu_over_RE = mu / R_E;
        double mu_over_r = mu / r;
        double potential_term = mu_over_RE - mu_over_r;
        double double_potential_term = two * potential_term;
        double v0_sq = v_orb_sq + double_potential_term;
        double v_0 = Math.sqrt(v0_sq);
        return v_0;
    }

}