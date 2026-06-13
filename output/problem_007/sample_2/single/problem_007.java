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
        double r_orbit = 8700000.0; // LengthQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity
        double seconds_per_hour = 3600.0; // DimensionlessQuantity
        int negative_one = -1; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_orbit = compute_orbital_speed(G, M_moon, r_orbit);
        double T_seconds = compute_period_seconds(two, pi, r_orbit, v_orbit);
        double T_hours = T_seconds / seconds_per_hour;
        double E_mech = compute_mechanical_energy(G, M_moon, m_spacecraft, two, r_orbit, negative_one);
        double v_esc = compute_escape_velocity(two, G, M_moon, R_moon);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_007\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"T_hours\": " + T_hours + ",");
        System.out.println("    \"E_mech\": " + E_mech + ",");
        System.out.println("    \"v_esc\": " + v_esc + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute circular orbital speed from gravitational attraction providing centripetal acceleration: v = sqrt(G*M/r). */
    public static double compute_orbital_speed(double G, double M_moon, double r_orbit) {
        double GM = G * M_moon;
        double v_orbit_sq = GM / r_orbit;
        double v_orbit = Math.sqrt(v_orbit_sq);
        return v_orbit;
    }

    /** Compute orbital period for circular motion using T = 2*pi*r / v. */
    public static double compute_period_seconds(int two, double pi, double r_orbit, double v_orbit) {
        double two_pi = two * pi;
        double orbit_circumference = two_pi * r_orbit;
        double T_seconds = orbit_circumference / v_orbit;
        return T_seconds;
    }

    /** Compute total mechanical energy in a circular orbit: E = -G*M*m/(2*r). */
    public static double compute_mechanical_energy(double G, double M_moon, double m_spacecraft, int two, double r_orbit, int negative_one) {
        double GM = G * M_moon;
        double GMm = GM * m_spacecraft;
        double two_r = two * r_orbit;
        double energy_magnitude = GMm / two_r;
        double E_mech = negative_one * energy_magnitude;
        return E_mech;
    }

    /** Compute lunar escape speed from the surface using v_esc = sqrt(2*G*M/R). */
    public static double compute_escape_velocity(int two, double G, double M_moon, double R_moon) {
        double two_G = two * G;
        double two_GM = two_G * M_moon;
        double v_esc_sq = two_GM / R_moon;
        double v_esc = Math.sqrt(v_esc_sq);
        return v_esc;
    }

}