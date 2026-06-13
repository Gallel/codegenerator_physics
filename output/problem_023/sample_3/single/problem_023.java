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

        // --- Main Execution Flow ---
        double piston_area = compute_circular_area(piston_diameter, pi, four);
        double rod_area = compute_circular_area(rod_diameter, pi, four);
        double return_area = piston_area - rod_area;
        double advance_force = compute_force(working_pressure, piston_area);
        double return_force = compute_force(working_pressure, return_area);
        double advance_volume = compute_volume(piston_area, stroke);
        double return_volume = compute_volume(return_area, stroke);
        double total_cycle_volume = advance_volume + return_volume;
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_023\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"advance_force\": " + advance_force + ",");
        System.out.println("    \"return_force\": " + return_force + ",");
        System.out.println("    \"advance_volume\": " + advance_volume + ",");
        System.out.println("    \"return_volume\": " + return_volume + ",");
        System.out.println("    \"total_cycle_volume\": " + total_cycle_volume + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Compute the cross-sectional area of a circle using A = (pi/4) * d^2. */
    public static double compute_circular_area(double diameter, double pi, int four) {
        double diameter_squared = Math.pow(diameter, four);
        double pi_times_diameter_squared = pi * diameter_squared;
        double area = pi_times_diameter_squared / four;
        return area;
    }

    /** Compute theoretical force from pressure acting on an area using F = P * A. */
    public static double compute_force(double pressure, double area) {
        double force = pressure * area;
        return force;
    }

    /** Compute chamber volume from cross-sectional area and stroke using V = A * L. */
    public static double compute_volume(double area, double stroke) {
        double volume = area * stroke;
        return volume;
    }

}