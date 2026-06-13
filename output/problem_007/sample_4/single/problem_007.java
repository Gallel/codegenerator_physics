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
        int five = 5; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity
        int three = 3; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity
        double seconds_per_hour = 3600.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double r_orbit = compute_orbital_radius(R_moon, five);
        double T_seconds = compute_orbital_period_seconds(r_orbit, G, M_moon, three, two, pi);
        double T_hours = convert_seconds_to_hours(T_seconds, seconds_per_hour);
        double E_mech = compute_mechanical_energy_circular_orbit(G, M_moon, m_spacecraft, two, r_orbit);
        double v_escape = compute_escape_velocity(two, G, M_moon, R_moon);
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

    /** Compute orbital radius from the Moon center as five lunar radii. */
    public static double compute_orbital_radius(double R_moon, int five) {
        double r_orbit = five * R_moon;
        return r_orbit;
    }

    /** Apply circular orbit period formula T = 2*pi*sqrt(r^3/(G*M)). */
    public static double compute_orbital_period_seconds(double r_orbit, double G, double M_moon, int three, int two, double pi) {
        double r_cubed = Math.pow(r_orbit, three);
        double GM = G * M_moon;
        double ratio = r_cubed / GM;
        double sqrt_ratio = Math.sqrt(ratio);
        double two_pi = two * pi;
        double T_seconds = two_pi * sqrt_ratio;
        return T_seconds;
    }

    /** Convert time from seconds to hours by dividing by 3600. */
    public static double convert_seconds_to_hours(double T_seconds, double seconds_per_hour) {
        double T_hours = T_seconds / seconds_per_hour;
        return T_hours;
    }

    /** Apply total mechanical energy formula for circular orbit E = -(G*M*m)/(2*r). */
    public static double compute_mechanical_energy_circular_orbit(double G, double M_moon, double m_spacecraft, int two, double r_orbit) {
        double GM = G * M_moon;
        double GMm = GM * m_spacecraft;
        double two_r = two * r_orbit;
        double E_positive_magnitude = GMm / two_r;
        double zero = 0.0;
        double E_mech = zero - E_positive_magnitude;
        return E_mech;
    }

    /** Apply escape speed formula v = sqrt(2*G*M/R) from the lunar surface and keep the positive root. */
    public static double compute_escape_velocity(int two, double G, double M_moon, double R_moon) {
        double twoG = two * G;
        double twoGM = twoG * M_moon;
        double escape_argument = twoGM / R_moon;
        double v_escape = Math.sqrt(escape_argument);
        return v_escape;
    }

}