public class problem_026 {

    public static void main(String[] args) {
        // Density = mass / volume, expressed in two units.
        double massGrams = 450;
        double volumeMl = 120;

        double densityGml = massGrams / volumeMl;
        double densityKgm3 = densityGml * 1000;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_026\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"density_g_ml\": " + densityGml + ",");
        System.out.println("    \"density_kg_m3\": " + densityKgm3 + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
