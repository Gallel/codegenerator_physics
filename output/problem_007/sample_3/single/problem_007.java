/**
 * Generated Physics-Validated Program: problem_007
 * Automatically generated from Modular DSL.
 */
public class problem_007 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m_spacecraft = 5000.0; // MassQuantity
        double M_moon = 7.35e+22; // MassQuantity
        double R_moon = 1740000.0; // LengthQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        double r_orbit = 8700000.0; // LengthQuantity
        int two = 2; // DimensionlessQuantity
        int three = 3; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity
        double seconds_per_hour = 3600.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double T_seconds = compute_period_seconds(r_orbit, G, M_moon, three, pi, two);
        double T_hours = T_seconds / seconds_per_hour;
        double E_mech = compute_mechanical_energy(G, M_moon, m_spacecraft, two, r_orbit);
        double v_escape = compute_escape_speed(two, G, M_moon, R_moon);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_007\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"T_hours\": " + T_hours + ",");
        System.out.println("    \"E_mech\": " + E_mech + ",");
        System.out.println("    \"v_escape\": " + v_escape + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply the circular-orbit period relation T = 2*pi*sqrt(r^3/(G*M)). */
    public static double compute_period_seconds(double r, double G_in, double M, int three_in, double pi_in, int two_in) {
        double r_cubed = Math.pow(r, three_in);
        double GM = G_in * M;
        double ratio = r_cubed / GM;
        double sqrt_ratio = Math.sqrt(ratio);
        double two_pi = two_in * pi_in;
        double T = two_pi * sqrt_ratio;
        return T;
    }

    /** Apply the circular-orbit mechanical energy formula E = -(G*M*m)/(2*r). */
    public static double compute_mechanical_energy(double G_in, double M, double m, int two_in, double r) {
        double GM = G_in * M;
        double GMm = GM * m;
        double two_r = two_in * r;
        double E_positive_magnitude = GMm / two_r;
        double zero = two_r - two_r;
        double E_mech = zero - E_positive_magnitude;
        return E_mech;
    }

    /** Apply the escape-speed formula v = +sqrt(2*G*M/R) from the lunar surface. */
    public static double compute_escape_speed(int two_in, double G_in, double M, double R) {
        double two_G = two_in * G_in;
        double numerator = two_G * M;
        double v_escape_sq = numerator / R;
        double v_escape = Math.sqrt(v_escape_sq);
        return v_escape;
    }

}