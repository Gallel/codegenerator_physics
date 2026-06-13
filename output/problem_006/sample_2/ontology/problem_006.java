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
        double r_orbit = compute_orbital_radius(R_E, h);
        double v_orbit = compute_orbital_speed(G, M_E, r_orbit);
        double T_orbit = compute_orbital_period(two, pi, r_orbit, v_orbit);
        double v0 = compute_launch_speed(two, G, M_E, R_E, r_orbit);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_006\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_orbit\": " + v_orbit + ",");
        System.out.println("    \"T_orbit\": " + T_orbit + ",");
        System.out.println("    \"v0\": " + v0 + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute orbital radius from Earth's center as the sum of Earth radius and orbital altitude. */
    public static double compute_orbital_radius(double R_E, double h) {
        double r_orbit = R_E + h;
        return r_orbit;
    }

    /** Compute circular orbital speed from v = sqrt(G*M_E/r_orbit). */
    public static double compute_orbital_speed(double G, double M_E, double r_orbit) {
        double GM = G * M_E;
        double v_orbit_sq = GM / r_orbit;
        double v_orbit = Math.sqrt(v_orbit_sq);
        return v_orbit;
    }

    /** Compute orbital period from T = 2*pi*r_orbit/v_orbit. */
    public static double compute_orbital_period(int two, double pi, double r_orbit, double v_orbit) {
        double two_pi = two * pi;
        double circumference = two_pi * r_orbit;
        double T_orbit = circumference / v_orbit;
        return T_orbit;
    }

    /** Compute the minimum launch speed from Earth's surface to reach the orbital radius with zero remaining radial speed using conservation of mechanical energy: v_0 = sqrt(2*G*M_E*(1/R_E - 1/r_orbit)). */
    public static double compute_launch_speed(int two, double G, double M_E, double R_E, double r_orbit) {
        double GM = G * M_E;
        double two_GM = two * GM;
        double inv_R_E = two / R_E;
        double inv_r_orbit = two / r_orbit;
        double radius_term = inv_R_E - inv_r_orbit;
        double v0_sq = two_GM * radius_term;
        double v0 = Math.sqrt(v0_sq);
        return v0;
    }

}