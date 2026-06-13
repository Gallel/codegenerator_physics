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
        double r = compute_orbital_radius(R_E, h);
        double mu = compute_gravitational_parameter(G, M_E);
        double E_i = compute_initial_energy(mu, m, R_E, K_i);
        double v_orb_sq = compute_orbital_speed_squared(mu, r);
        double v_orb = Math.sqrt(v_orb_sq);
        double E_f = compute_final_orbital_energy(mu, m, r, two, K_i);
        double DeltaE = compute_energy_required(E_f, E_i);
        double T = compute_orbital_period(two, pi, r, v_orb);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_002\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"DeltaE\": " + DeltaE + ",");
        System.out.println("    \"v_orb\": " + v_orb + ",");
        System.out.println("    \"T\": " + T + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute orbital radius from Earth's center as the sum of Earth radius and orbital altitude. */
    public static double compute_orbital_radius(double R_E, double h) {
        double r = R_E + h;
        return r;
    }

    /** Compute the gravitational parameter mu = G*M_E. */
    public static double compute_gravitational_parameter(double G, double M_E) {
        double mu = G * M_E;
        return mu;
    }

    /** Compute the initial total mechanical energy at Earth's surface with neglected initial kinetic energy: E_i = -mu*m/R_E. */
    public static double compute_initial_energy(double mu, double m, double R_E, double K_i) {
        double mu_m_i = mu * m;
        double mu_m_over_R_E = mu_m_i / R_E;
        double E_i = K_i - mu_m_over_R_E;
        return E_i;
    }

    /** Use the circular-orbit relation to compute v_orb^2 = mu/r. */
    public static double compute_orbital_speed_squared(double mu, double r) {
        double v_orb_sq = mu / r;
        return v_orb_sq;
    }

    /** Compute the total mechanical energy in circular orbit using E_f = -mu*m/(2r). */
    public static double compute_final_orbital_energy(double mu, double m, double r, int two) {
        double mu_m_f = mu * m;
        double two_r = two * r;
        double mu_m_over_2r = mu_m_f / two_r;
        double E_f = K_i - mu_m_over_2r;
        return E_f;
    }

    /** Compute the external energy required as the increase in total mechanical energy: DeltaE = E_f - E_i. */
    public static double compute_energy_required(double E_f, double E_i) {
        double DeltaE = E_f - E_i;
        return DeltaE;
    }

    /** Compute the orbital period from uniform circular motion: T = 2*pi*r / v_orb. */
    public static double compute_orbital_period(int two, double pi, double r, double v_orb) {
        double two_pi = two * pi;
        double two_pi_r = two_pi * r;
        double T = two_pi_r / v_orb;
        return T;
    }

}