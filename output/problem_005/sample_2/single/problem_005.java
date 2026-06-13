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
        double r_sep = 1120.0; // LengthQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity
        int three = 3; // DimensionlessQuantity
        int four = 4; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double r_didymos = radius_from_diameter(d, two);
        double V_didymos = sphere_volume(r_didymos, four, three, pi);
        double M_didymos = mass_from_density_volume(rho, V_didymos);
        double g_surface = surface_gravity(G, M_didymos, r_didymos, two);
        double F_on_dimorphos = gravitational_force(G, M_didymos, m_dimorphos, r_sep, two);
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

    /** Convert diameter to radius using r = d/2. */
    public static double radius_from_diameter(double d_in, int two_in) {
        double r_out = d_in / two_in;
        return r_out;
    }

    /** Compute spherical volume with V = (4/3) * pi * r^3. */
    public static double sphere_volume(double r_in, int four_in, int three_in, double pi_in) {
        double r_cubed = Math.pow(r_in, three_in);
        double four_pi = four_in * pi_in;
        double factor = four_pi / three_in;
        double V_out = factor * r_cubed;
        return V_out;
    }

    /** Compute mass from density and volume using M = rho * V. */
    public static double mass_from_density_volume(double rho_in, double V_in) {
        double M_out = rho_in * V_in;
        return M_out;
    }

    /** Compute surface gravitational acceleration magnitude with g = G*M/r^2. */
    public static double surface_gravity(double G_in, double M_in, double r_in, int two_in) {
        double r_sq = Math.pow(r_in, two_in);
        double GM = G_in * M_in;
        double g_out = GM / r_sq;
        return g_out;
    }

    /** Compute gravitational force magnitude with F = G*M*m/r^2. */
    public static double gravitational_force(double G_in, double M_in, double m_in, double r_in, int two_in) {
        double GM = G_in * M_in;
        double GMm = GM * m_in;
        double r_sq = Math.pow(r_in, two_in);
        double F_out = GMm / r_sq;
        return F_out;
    }

}