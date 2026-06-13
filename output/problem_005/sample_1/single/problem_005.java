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
        double r = compute_radius(d, two);
        double M = compute_mass_from_density(r, rho, four, three, pi);
        double g_surface = compute_surface_gravity(G, M, r, two);
        double F = compute_gravitational_force(G, M, m_dimorphos, r_orbit, two);
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

    /** Model Didymos as a sphere, compute its volume V = (4/3) * pi * r^3, then compute mass M = rho * V. */
    public static double compute_mass_from_density(double r, double rho, int four, int three, double pi) {
        double r_cubed = Math.pow(r, three);
        double four_pi = four * pi;
        double numerator = four_pi * r_cubed;
        double V = numerator / three;
        double M = rho * V;
        return M;
    }

    /** Compute the gravitational acceleration at the surface using g_surface = G * M / r^2. */
    public static double compute_surface_gravity(double G, double M, double r, int two) {
        double GM = G * M;
        double r_squared = Math.pow(r, two);
        double g_surface = GM / r_squared;
        return g_surface;
    }

    /** Compute the gravitational force magnitude on Dimorphos using F = G * M * m_dimorphos / r_orbit^2. */
    public static double compute_gravitational_force(double G, double M, double m_dimorphos, double r_orbit, int two) {
        double GM = G * M;
        double GMm = GM * m_dimorphos;
        double r_orbit_squared = Math.pow(r_orbit, two);
        double F = GMm / r_orbit_squared;
        return F;
    }

}