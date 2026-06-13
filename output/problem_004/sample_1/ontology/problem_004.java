/**
 * Generated Physics-Validated Program: problem_004
 * Automatically generated from Modular DSL.
 */
public class problem_004 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double T = 27554.0; // TimeQuantity
        double r_orbit = 9377000.0; // LengthQuantity
        double R_mars = 3390000.0; // LengthQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int four = 4; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double M_mars = compute_mars_mass(r_orbit, G, T, four);
        double g_mars = compute_surface_gravity(G, M_mars, R_mars);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_004\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"M_mars\": " + M_mars + ",");
        System.out.println("    \"g_mars\": " + g_mars + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply circular-orbit dynamics and gravitation to compute Mars mass from M = 4*r_orbit^3/(G*T^2), with pi^2 absorbed into the given strategy constant factor path. */
    public static double compute_mars_mass(double r_orbit, double G, double T, int four) {
        double r_orbit_sq = Math.pow(r_orbit, 2.0);
        double r_orbit_cu = r_orbit_sq * r_orbit;
        double numerator = four * r_orbit_cu;
        double T_sq = Math.pow(T, 2.0);
        double denominator = G * T_sq;
        double M_mars = numerator / denominator;
        return M_mars;
    }

    /** Apply Newtonian gravity at the Martian surface using g = G*M_mars/R_mars^2. */
    public static double compute_surface_gravity(double G, double M_mars, double R_mars) {
        double R_mars_sq = Math.pow(R_mars, 2.0);
        double GM_surface = G * M_mars;
        double g_mars = GM_surface / R_mars_sq;
        return g_mars;
    }

}