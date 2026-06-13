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
        double r_orbit = 1120.0; // LengthQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity
        int three = 3; // DimensionlessQuantity
        int four = 4; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double r_didymos = compute_radius(d, two);
        double V_didymos = compute_sphere_volume(four, three, pi, r_didymos);
        double M_didymos = compute_mass_from_density_volume(rho, V_didymos);
        double g_surface = compute_surface_gravity(G, M_didymos, r_didymos, two);
        double F_on_dimorphos = compute_gravitational_force(G, M_didymos, m_dimorphos, r_orbit, two);
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

    /** Compute the radius from the diameter using r = d/2. */
    public static double compute_radius(double d_in, int two_in) {
        double r = d_in / two_in;
        return r;
    }

    /** Compute the volume of a sphere using V = (4/3) * pi * r^3. */
    public static double compute_sphere_volume(int four_in, int three_in, double pi_in, double r_in) {
        double four_thirds = four_in / three_in;
        double r_cubed = Math.pow(r_in, three_in);
        double coeff = four_thirds * pi_in;
        double V = coeff * r_cubed;
        return V;
    }

    /** Compute mass from density and volume using M = rho * V. */
    public static double compute_mass_from_density_volume(double rho_in, double V_in) {
        double M = rho_in * V_in;
        return M;
    }

    /** Compute gravitational acceleration at the surface using g = G * M / r^2. */
    public static double compute_surface_gravity(double G_in, double M_in, double r_surface_in, int two_in) {
        double GM = G_in * M_in;
        double r_surface_sq = Math.pow(r_surface_in, two_in);
        double g_surface = GM / r_surface_sq;
        return g_surface;
    }

    /** Compute gravitational force magnitude using F = G * M * m / r^2. */
    public static double compute_gravitational_force(double G_in, double M_in, double m_in, double r_in, int two_in) {
        double GM = G_in * M_in;
        double GMm = GM * m_in;
        double r_sq = Math.pow(r_in, two_in);
        double F = GMm / r_sq;
        return F;
    }

}