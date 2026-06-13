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
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double M_mars = compute_mars_mass(r_orbit, T, G, four, two);
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

    /** Apply the circular-orbit relation derived from gravitational force providing centripetal acceleration: M_mars = 4*pi^2*r_orbit^3/(G*T^2). */
    public static double compute_mars_mass(double r_orbit, double T, double G, int four, int two) {
        double r_sq = r_orbit * r_orbit;
        double r_cu = r_sq * r_orbit;
        double T_sq = Math.pow(T, two);
        double four_r_cu = four * r_cu;
        double den_mass = G * T_sq;
        double M_mars = four_r_cu / den_mass;
        return M_mars;
    }

    /** Apply Newton's law for gravitational acceleration at the Martian surface: g_mars = G*M_mars/R_mars^2. */
    public static double compute_surface_gravity(double G, double M_mars, double R_mars, int two) {
        double GM = G * M_mars;
        double R_sq = Math.pow(R_mars, two);
        double g_mars = GM / R_sq;
        return g_mars;
    }

}