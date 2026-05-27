public class problem_018 {

    public static void main(String[] args) {
        // Mechanical energy = kinetic + gravitational potential.
        double mass = 15000;
        double v = 900 / 3.6;
        double h = 10000;
        double g = 9.8;

        double kineticEnergy = 0.5 * mass * v * v;
        double potentialEnergy = mass * g * h;
        double mechanicalEnergy = kineticEnergy + potentialEnergy;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_018\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"kinetic_energy\": " + kineticEnergy + ",");
        System.out.println("    \"gravitational_potential_energy\": " + potentialEnergy + ",");
        System.out.println("    \"mechanical_energy\": " + mechanicalEnergy + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
