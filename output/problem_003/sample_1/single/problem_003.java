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
        int two = 2; // DimensionlessQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double orbital_velocity = compute_orbital_speed(G, M_earth, r);
        double orbital_period = compute_orbital_period(two, pi, r, orbital_velocity);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_003\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"orbital_velocity\": " + orbital_velocity + ",");
        System.out.println("    \"orbital_period\": " + orbital_period + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply circular-orbit dynamics from equating gravitational and centripetal effects to compute orbital speed magnitude: v = sqrt(G*M_earth/r). */
    public static double compute_orbital_speed(double G, double M_earth, double r) {
        double GM = G * M_earth;
        double GM_over_r = GM / r;
        double v = Math.sqrt(GM_over_r);
        return v;
    }

    /** Compute one-orbit period for uniform circular motion using circumference divided by orbital speed: T = 2*pi*r/v. */
    public static double compute_orbital_period(int two, double pi, double r, double v) {
        double two_pi = two * pi;
        double C = two_pi * r;
        double T = C / v;
        return T;
    }

}