/**
 * Generated Physics-Validated Program: problem_002
 * Automatically generated from Modular DSL.
 */
public class problem_002 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m = 2000.0; // MassQuantity
        double h = 36000000.0; // LengthQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType
        double R_E = 6370000.0; // LengthQuantity
        double M_E = 5.972e+24; // MassQuantity
        double K_i = 0.0; // EnergyQuantity
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double r_f = compute_orbital_radius(R_E, h);
        double v = compute_orbital_speed(G, M_E, r_f);
        double E_i = compute_initial_energy(G, M_E, m, R_E, K_i);
        double E_f = compute_final_orbital_energy(G, M_E, m, r_f, two);
        double Delta_E = compute_energy_required(E_f, E_i);
        double T = compute_orbital_period(two, pi, r_f, v);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_002\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"Delta_E\": " + Delta_E + ",");
        System.out.println("    \"v\": " + v + ",");
        System.out.println("    \"T\": " + T + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute orbital radius from Earth's center as the sum of Earth radius and orbital altitude. */
    public static double compute_orbital_radius(double R_E, double h) {
        double r_f = R_E + h;
        return r_f;
    }

    /** Compute circular orbital speed from gravitational force providing centripetal force: v = sqrt(G*M_E/r_f). */
    public static double compute_orbital_speed(double G, double M_E, double r_f) {
        double GM = G * M_E;
        double GM_over_r = GM / r_f;
        double v = Math.sqrt(GM_over_r);
        return v;
    }

    /** Compute initial mechanical energy at Earth's surface with neglected initial kinetic energy: E_i = -G*M_E*m/R_E + K_i. */
    public static double compute_initial_energy(double G, double M_E, double m, double R_E, double K_i) {
        double GM = G * M_E;
        double GMm = GM * m;
        double GMm_over_R_E = GMm / R_E;
        double E_i = K_i - GMm_over_R_E;
        return E_i;
    }

    /** Compute final mechanical energy in circular orbit using E_f = -G*M_E*m/(2*r_f). */
    public static double compute_final_orbital_energy(double G, double M_E, double m, double r_f, int two) {
        double GM = G * M_E;
        double GMm = GM * m;
        double two_r_f = two * r_f;
        double GMm_over_2r = GMm / two_r_f;
        double E_f = 0.0 - GMm_over_2r;
        return E_f;
    }

    /** Compute supplied energy as the increase in mechanical energy: Delta_E = E_f - E_i. */
    public static double compute_energy_required(double E_f, double E_i) {
        double Delta_E = E_f - E_i;
        return Delta_E;
    }

    /** Compute orbital period for uniform circular motion: T = 2*pi*r_f/v. */
    public static double compute_orbital_period(int two, double pi, double r_f, double v) {
        double two_pi = two * pi;
        double two_pi_r = two_pi * r_f;
        double T = two_pi_r / v;
        return T;
    }

}