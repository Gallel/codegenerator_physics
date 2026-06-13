/**
 * Generated Physics-Validated Program: problem_023
 * Automatically generated from Modular DSL.
 */
public class problem_023 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double piston_diameter = 0.07; // LengthQuantity
        double rod_diameter = 0.025; // LengthQuantity
        double stroke = 0.1; // LengthQuantity
        double working_pressure = 600000.0; // PressureQuantity
        double pi = 3.141592653589793; // DimensionlessQuantity
        int four = 4; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double A_piston = compute_circular_area(piston_diameter, pi, four, two);
        double A_rod = compute_circular_area(rod_diameter, pi, four, two);
        double A_return = compute_return_area(A_piston, A_rod);
        double F_advance = compute_force(working_pressure, A_piston);
        double F_return = compute_force(working_pressure, A_return);
        double V_advance = compute_volume(A_piston, stroke);
        double V_return = compute_volume(A_return, stroke);
        double V_total = V_advance + V_return;
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_023\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"F_advance\": " + F_advance + ",");
        System.out.println("    \"F_return\": " + F_return + ",");
        System.out.println("    \"V_advance\": " + V_advance + ",");
        System.out.println("    \"V_return\": " + V_return + ",");
        System.out.println("    \"V_total\": " + V_total + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Calculate circular cross-sectional area using A = (pi/4) d^2. */
    public static double compute_circular_area(double diameter, double pi, int four, int two) {
        double diameter_squared = Math.pow(diameter, two);
        double pi_times_d2 = pi * diameter_squared;
        double area = pi_times_d2 / four;
        return area;
    }

    /** Calculate annular return area by subtracting rod area from piston area. */
    public static double compute_return_area(double A_piston, double A_rod) {
        double A_return = A_piston - A_rod;
        return A_return;
    }

    /** Calculate theoretical force using F = pA. */
    public static double compute_force(double pressure, double area) {
        double force = pressure * area;
        return force;
    }

    /** Calculate stroke volume using V = A times stroke. */
    public static double compute_volume(double area, double stroke) {
        double volume = area * stroke;
        return volume;
    }

}