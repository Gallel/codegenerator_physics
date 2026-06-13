/**
 * Generated Physics-Validated Program: problem_005
 * Automatically generated from Modular DSL.
 */
public class problem_005 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double d = 781.0; // LengthQuantity
        double rho = 2146.0; // DensityQuantity
        double m_dimorphos = 44200000000.0; // MassQuantity
        double r_dimorphos = 1120.0; // LengthQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity
        int three = 3; // DimensionlessQuantity
        int four = 4; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double R = compute_radius(d, two);
        double V = compute_volume(R, four, three, pi);
        double M_didymos = compute_mass(rho, V);
        double g_surface = compute_surface_gravity(G, M_didymos, R, two);
        double F_on_dimorphos = compute_gravitational_force(G, M_didymos, m_dimorphos, r_dimorphos, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_005\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"M_didymos\": " + M_didymos + ",");
        System.out.println("    \"g_surface\": " + g_surface + ",");
        System.out.println("    \"F_on_dimorphos\": " + F_on_dimorphos + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute the radius of Didymos from its diameter using R = d/2. */
    public static double compute_radius(double d_in, int two_in) {
        double R = d_in / two_in;
        return R;
    }

    /** Compute the spherical volume using V = (4/3) * pi * R^3. */
    public static double compute_volume(double R_in, int four_in, int three_in, double pi_in) {
        double R_cubed = Math.pow(R_in, three_in);
        double four_pi = four_in * pi_in;
        double numerator = four_pi * R_cubed;
        double V = numerator / three_in;
        return V;
    }

    /** Compute the mass from density and volume using M = rho * V. */
    public static double compute_mass(double rho_in, double V_in) {
        double M = rho_in * V_in;
        return M;
    }

    /** Compute the gravitational acceleration magnitude at the surface using g = G * M / R^2. */
    public static double compute_surface_gravity(double G_in, double M_in, double R_in, int two_in) {
        double R_squared = Math.pow(R_in, two_in);
        double GM = G_in * M_in;
        double g_surface = GM / R_squared;
        return g_surface;
    }

    /** Compute the gravitational force magnitude on Dimorphos using F = G * M * m_dimorphos / r^2. */
    public static double compute_gravitational_force(double G_in, double M_in, double m_in, double r_in, int two_in) {
        double GM = G_in * M_in;
        double GMm = GM * m_in;
        double r_squared = Math.pow(r_in, two_in);
        double F_grav = GMm / r_squared;
        return F_grav;
    }

}