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
        double pi = 3.141592653589793; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity
        int four = 4; // DimensionlessQuantity
        int three = 3; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double M_mars = compute_mars_mass(pi, four, r_orbit, three, G, T, two);
        double g_mars = compute_surface_gravity(G, M_mars, R_mars, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_004\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"M_mars\": " + M_mars + ",");
        System.out.println("    \"g_mars\": " + g_mars + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply circular-orbit dynamics and gravitation: M_mars = 4*pi^2*r_orbit^3/(G*T^2). */
    public static double compute_mars_mass(double pi, int four, double r_orbit, int three, double G, double T, int two) {
        double pi_sq = Math.pow(pi, two);
        double four_pi_sq = four * pi_sq;
        double r_orbit_cu = Math.pow(r_orbit, three);
        double numerator = four_pi_sq * r_orbit_cu;
        double T_sq = Math.pow(T, two);
        double denominator = G * T_sq;
        double M_mars = numerator / denominator;
        return M_mars;
    }

    /** Apply Newtonian gravity at the Martian surface: g_mars = G*M_mars/R_mars^2. */
    public static double compute_surface_gravity(double G, double M_mars, double R_mars, int two) {
        double GM = G * M_mars;
        double R_mars_sq = Math.pow(R_mars, two);
        double g_mars = GM / R_mars_sq;
        return g_mars;
    }

}