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
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double r = compute_orbital_radius(R_E, h);
        double U_i = compute_initial_potential_energy(G, M_E, m, R_E);
        double v_sq = compute_orbital_speed(G, M_E, r);
        double v = Math.sqrt(v_sq);
        double E_f = compute_final_mechanical_energy(G, M_E, m, r, two);
        double Delta_E = compute_energy_required(E_f, U_i);
        double T = compute_orbital_period(two, pi, r, v);
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
        double r = R_E + h;
        return r;
    }

    /** Compute initial gravitational potential energy at Earth's surface using U_i = -G M_E m / R_E. */
    public static double compute_initial_potential_energy(double G, double M_E, double m, double R_E) {
        double GM = G * M_E;
        double GMm = GM * m;
        double Ui_mag = GMm / R_E;
        double zero_temp = Ui_mag - Ui_mag;
        double U_i = zero_temp - Ui_mag;
        return U_i;
    }

    /** Compute circular orbital speed from v = sqrt(G M_E / r), returning the radicand for a positive root in execution flow. */
    public static double compute_orbital_speed(double G, double M_E, double r) {
        double GM = G * M_E;
        double v_sq = GM / r;
        return v_sq;
    }

    /** Compute final total mechanical energy in circular orbit using E_f = -G M_E m / (2r). */
    public static double compute_final_mechanical_energy(double G, double M_E, double m, double r, int two) {
        double GM = G * M_E;
        double GMm = GM * m;
        double two_r = two * r;
        double Ef_mag = GMm / two_r;
        double zero_temp = Ef_mag - Ef_mag;
        double E_f = zero_temp - Ef_mag;
        return E_f;
    }

    /** Compute required supplied energy as the increase in mechanical energy Delta_E = E_f - E_i, with E_i = U_i because initial kinetic energy is neglected. */
    public static double compute_energy_required(double E_f, double U_i) {
        double Delta_E = E_f - U_i;
        return Delta_E;
    }

    /** Compute orbital period for uniform circular motion using T = 2 pi r / v. */
    public static double compute_orbital_period(int two, double pi, double r, double v) {
        double two_pi = two * pi;
        double circumference = two_pi * r;
        double T = circumference / v;
        return T;
    }

}