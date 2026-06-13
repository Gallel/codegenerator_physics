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
        double seconds_per_hour = 3600.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double T_seconds = compute_orbital_period_seconds(r_orbit, G, M_moon, two, three);
        double T_hours = convert_seconds_to_hours(T_seconds, seconds_per_hour);
        double E_mech = compute_mechanical_energy_circular_orbit(G, M_moon, m_spacecraft, r_orbit, two);
        double v_escape_sq = compute_escape_velocity_squared(G, M_moon, R_moon, two);
        double v_escape = Math.sqrt(v_escape_sq);
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

    /** Apply the circular orbit period relation T = 2*pi*sqrt(r^3/(G*M)). */
    public static double compute_orbital_period_seconds(double r, double G_in, double M, int two_in, int three_in) {
        double r_cubed = Math.pow(r, three_in);
        double GM = G_in * M;
        double period_argument = r_cubed / GM;
        double sqrt_term = Math.sqrt(period_argument);
        double T_seconds = two_in * sqrt_term;
        return T_seconds;
    }

    /** Convert time from seconds to hours by dividing by 3600. */
    public static double convert_seconds_to_hours(double time_seconds, double sec_per_hour) {
        double T_hours = time_seconds / sec_per_hour;
        return T_hours;
    }

    /** Apply the total mechanical energy formula for a circular orbit E = -(G*M*m)/(2*r). */
    public static double compute_mechanical_energy_circular_orbit(double G_in, double M, double m, double r, int two_in) {
        double GM = G_in * M;
        double GMm = GM * m;
        double two_r = two_in * r;
        double energy_magnitude = GMm / two_r;
        double zero = r - r;
        double E_mech = zero - energy_magnitude;
        return E_mech;
    }

    /** Apply the escape speed relation in squared form v^2 = 2GM/R from energy conservation at the lunar surface. */
    public static double compute_escape_velocity_squared(double G_in, double M, double R, int two_in) {
        double GM = G_in * M;
        double two_GM = two_in * GM;
        double v_escape_sq = two_GM / R;
        return v_escape_sq;
    }

}