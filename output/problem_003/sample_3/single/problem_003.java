/**
 * Generated Physics-Validated Program: problem_003
 * Automatically generated from Modular DSL.
 */
public class problem_003 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double r = 384000000.0; // LengthQuantity
        double M_earth = 5.972e+24; // MassQuantity
        double G = 6.67e-11; // UniversalGravitationalConstantType

        // --- Main Execution Flow ---
        double two = 0.0;
        double pi = 0.0;
        double v_squared = compute_orbital_speed_squared(G, M_earth, r);
        double v = Math.sqrt(v_squared);
        double T = compute_orbital_period(r, v, two, pi);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_003\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v\": " + v + ",");
        System.out.println("    \"T\": " + T + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply circular-orbit force balance to compute v^2 = G*M_earth/r before taking the positive square root for orbital speed. */
    public static double compute_orbital_speed_squared(double G, double M_earth, double r) {
        double GM = G * M_earth;
        double v_squared = GM / r;
        return v_squared;
    }

    /** Compute orbital period from uniform circular motion using T = 2*pi*r/v. */
    public static double compute_orbital_period(double r, double v, double two, double pi) {
        double two_pi = two * pi;
        double circumference = two_pi * r;
        double T = circumference / v;
        return T;
    }

}