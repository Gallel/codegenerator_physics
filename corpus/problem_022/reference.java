public class problem_022 {

    public static void main(String[] args) {
        // Kinetic energy.
        double mass = 1300;
        double v = 30;

        double kineticEnergy = 0.5 * mass * v * v;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_022\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"kinetic_energy\": " + kineticEnergy + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
