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
        int three = 3; // DimensionlessQuantity
        int four = 4; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double M_mars = compute_mars_mass(r_orbit, T, G, pi, two, three, four);
        double g_surface = compute_surface_gravity(G, M_mars, R_mars, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_004\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"M_mars\": " + M_mars + ",");
        System.out.println("    \"g_surface\": " + g_surface + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply circular-orbit dynamics and Newtonian gravitation to compute Mars's mass from Phobos's orbital radius and period: M = 4*pi^2*r^3/(G*T^2). */
    public static double compute_mars_mass(double r, double T, double G, double pi, int two, int three, int four) {
        double pi_sq = Math.pow(pi, two);
        double r_cu = Math.pow(r, three);
        double four_pi_sq = four * pi_sq;
        double numerator = four_pi_sq * r_cu;
        double T_sq = Math.pow(T, two);
        double denominator = G * T_sq;
        double M_mars = numerator / denominator;
        return M_mars;
    }

    /** Apply Newton's law of gravitation at the Martian surface: g = G*M/R^2. */
    public static double compute_surface_gravity(double G, double M, double R, int two) {
        double GM = G * M;
        double R_sq = Math.pow(R, two);
        double g_surface = GM / R_sq;
        return g_surface;
    }

}