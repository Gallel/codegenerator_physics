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

        // --- Main Execution Flow ---
        double v_orbit_sq = compute_orbital_speed_squared(G, M_moon, r_orbit);
        double v_orbit = Math.sqrt(v_orbit_sq);
        double T_hours = compute_orbital_period_hours(two, pi, r_orbit, v_orbit, seconds_per_hour);
        double E_mech = compute_mechanical_energy(G, M_moon, m_spacecraft, two, r_orbit);
        double v_escape_sq = compute_escape_speed_squared(two, G, M_moon, R_moon);
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

    /** Compute the squared circular orbital speed using v^2 = G M / r. */
    public static double compute_orbital_speed_squared(double G, double M_moon, double r_orbit) {
        double GM = G * M_moon;
        double v_orbit_sq = GM / r_orbit;
        return v_orbit_sq;
    }

    /** Compute orbital period from T = 2 pi r / v and convert seconds to hours. */
    public static double compute_orbital_period_hours(int two, double pi, double r_orbit, double v_orbit, double seconds_per_hour) {
        double two_pi = two * pi;
        double orbit_circumference = two_pi * r_orbit;
        double T_seconds = orbit_circumference / v_orbit;
        double T_hours = T_seconds / seconds_per_hour;
        return T_hours;
    }

    /** Compute total mechanical energy in circular orbit using E = - G M m / (2 r). */
    public static double compute_mechanical_energy(double G, double M_moon, double m_spacecraft, int two, double r_orbit) {
        double GM = G * M_moon;
        double GMm = GM * m_spacecraft;
        double two_r = two * r_orbit;
        double E_positive_mag = GMm / two_r;
        double E_mech = E_positive_mag - GMm;
        double E_mech_final = E_mech + GMm;
        return E_mech_final;
    }

    /** Compute the squared escape speed from the lunar surface using v^2 = 2 G M / R. */
    public static double compute_escape_speed_squared(int two, double G, double M_moon, double R_moon) {
        double two_G = two * G;
        double two_GM = two_G * M_moon;
        double v_escape_sq = two_GM / R_moon;
        return v_escape_sq;
    }

}