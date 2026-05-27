public class problem_001 {

    public static void main(String[] args) {
        // Phobos in circular orbit around Mars: K = G*M*m/(2r), E = -K.
        double G = 6.67e-11;
        double massMars = 6.39e23;
        double massPhobos = 1.08e16;
        double r = 9377e3;

        double kineticEnergy = G * massMars * massPhobos / (2 * r);
        double mechanicalEnergy = -kineticEnergy;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_001\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"kinetic_energy\": " + kineticEnergy + ",");
        System.out.println("    \"mechanical_energy\": " + mechanicalEnergy + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
