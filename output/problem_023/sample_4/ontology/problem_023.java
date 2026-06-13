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
        double pi_over_4 = 0.7853981633974483; // DimensionlessQuantity
        int two = 2; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double piston_area = compute_circular_area(piston_diameter, pi_over_4, two);
        double rod_area = compute_circular_area(rod_diameter, pi_over_4, two);
        double annular_area = compute_annular_area(piston_area, rod_area);
        double advance_force = compute_force(working_pressure, piston_area);
        double return_force = compute_force(working_pressure, annular_area);
        double advance_volume = compute_volume(piston_area, stroke);
        double return_volume = compute_volume(annular_area, stroke);
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

    /** Compute circular cross-sectional area using A = (pi/4) d^2. */
    public static double compute_circular_area(double diameter, double pi_over_4, int two) {
        double diameter_squared = Math.pow(diameter, two);
        double area = pi_over_4 * diameter_squared;
        return area;
    }

    /** Compute effective return-side annular area as piston area minus rod area. */
    public static double compute_annular_area(double piston_area, double rod_area) {
        double annular_area = piston_area - rod_area;
        return annular_area;
    }

    /** Compute theoretical force from pressure acting on area using F = pA. */
    public static double compute_force(double pressure, double area) {
        double force = pressure * area;
        return force;
    }

    /** Compute admitted air volume as swept volume V = AL. */
    public static double compute_volume(double area, double stroke) {
        double volume = area * stroke;
        return volume;
    }

}