public class problem_020 {

    public static void main(String[] args) {
        // Mechanical energy at height, then final speed by energy conservation.
        double mass = 0.150;
        double v0 = 3;
        double h = 8;
        double g = 9.8;

        double mechanicalEnergy = 0.5 * mass * v0 * v0 + mass * g * h;
        double finalVelocity = Math.sqrt(2 * mechanicalEnergy / mass);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_020\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"initial_mechanical_energy\": " + mechanicalEnergy + ",");
        System.out.println("    \"final_velocity\": " + finalVelocity + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
