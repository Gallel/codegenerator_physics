public class problem_012 {

    public static void main(String[] args) {
        // Free fall: v^2 = 2*g*h  ->  h = v^2 / (2g).
        double g = 9.8;
        double v = 54 / 3.6;

        double fallHeight = v * v / (2 * g);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_012\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"fall_height\": " + fallHeight + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
