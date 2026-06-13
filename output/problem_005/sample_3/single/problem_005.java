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
        double r = compute_radius(d, two);
        double V = compute_sphere_volume(r, four, three, pi);
        double M = compute_mass(rho, V);
        double g_surface = compute_surface_gravity(G, M, r, two);
        double F = compute_gravitational_force(G, M, m_dimorphos, r_sep, two);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_005\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"M\": " + M + ",");
        System.out.println("    \"g_surface\": " + g_surface + ",");
        System.out.println("    \"F\": " + F + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute the radius from the diameter using r = d/2. */
    public static double compute_radius(double d, int two) {
        double r = d / two;
        return r;
    }

    /** Compute the volume of a sphere using V = (4/3) * pi * r^3. */
    public static double compute_sphere_volume(double r, int four, int three, double pi) {
        double r_cubed = Math.pow(r, three);
        double four_pi = four * pi;
        double factor = four_pi / three;
        double V = factor * r_cubed;
        return V;
    }

    /** Compute mass from density and volume using M = rho * V. */
    public static double compute_mass(double rho, double V) {
        double M = rho * V;
        return M;
    }

    /** Compute gravitational acceleration at the surface using g = G * M / r^2. */
    public static double compute_surface_gravity(double G, double M, double r, int two) {
        double GM = G * M;
        double r_squared = Math.pow(r, two);
        double g_surface = GM / r_squared;
        return g_surface;
    }

    /** Compute gravitational force magnitude using F = G * M * m_dimorphos / r_sep^2. */
    public static double compute_gravitational_force(double G, double M, double m_dimorphos, double r_sep, int two) {
        double GM = G * M;
        double GMm = GM * m_dimorphos;
        double r_sep_squared = Math.pow(r_sep, two);
        double F = GMm / r_sep_squared;
        return F;
    }

}