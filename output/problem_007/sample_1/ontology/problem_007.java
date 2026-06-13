/**
 * Generated Physics-Validated Program: problem_007
 * Automatically generated from Modular DSL.
 */
public class problem_007 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m_sc = 5000.0; // MassQuantity
        double M_moon = 7.35e+22; // MassQuantity
        double R_moon = 1740000.0; // LengthQuantity
        double r_orbit = 8700000.0; // LengthQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity
        int three = 3; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity
        double seconds_per_hour = 3600.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double T_seconds = compute_orbital_period_seconds(r_orbit, G, M_moon, two, three, pi);
        double T_hours = T_seconds / seconds_per_hour;
        double E_mech = compute_mechanical_energy(G, M_moon, m_sc, r_orbit, two);
        double v_escape = compute_escape_speed(G, M_moon, R_moon, two);
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

    /** Apply the circular-orbit period formula T = 2*pi*sqrt(r^3/(G*M)). */
    public static double compute_orbital_period_seconds(double r, double G_in, double M, int two_in, int three_in, double pi_in) {
        double r_cubed = Math.pow(r, three_in);
        double GM = G_in * M;
        double period_argument = r_cubed / GM;
        double sqrt_term = Math.sqrt(period_argument);
        double two_pi = two_in * pi_in;
        double T_seconds = two_pi * sqrt_term;
        return T_seconds;
    }

    /** Apply the total mechanical energy formula for a circular orbit E = -(G*M*m)/(2*r). */
    public static double compute_mechanical_energy(double G_in, double M, double m, double r, int two_in) {
        double GM = G_in * M;
        double GMm = GM * m;
        double two_r = two_in * r;
        double E_magnitude = GMm / two_r;
        double zero_ref = two_r - two_r;
        double E_mech = zero_ref - E_magnitude;
        return E_mech;
    }

    /** Apply energy conservation for escape from the lunar surface: v_esc = sqrt(2*G*M/R). Use the positive root only because the result is a speed magnitude. */
    public static double compute_escape_speed(double G_in, double M, double R, int two_in) {
        double twoG = two_in * G_in;
        double numerator = twoG * M;
        double escape_argument = numerator / R;
        double v_escape = Math.sqrt(escape_argument);
        return v_escape;
    }

}