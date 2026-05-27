public class problem_027 {

    public static void main(String[] args) {
        // Hydraulic press: equal pressure on both pistons. F1 = F2 * S1 / S2.
        double areaLarge = 250e-4;
        double areaSmall = 10e-4;
        double loadLarge = 12000;

        double pressure = loadLarge / areaLarge;
        double forceSmall = pressure * areaSmall;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_027\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"force_small_piston\": " + forceSmall + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
