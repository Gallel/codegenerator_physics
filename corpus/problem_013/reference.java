public class problem_013 {

    public static void main(String[] args) {
        // Vertical throw: at the top v = 0.
        double g = 9.8;
        double v0 = 15;

        double timeToTop = v0 / g;
        double maxHeight = v0 * v0 / (2 * g);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_013\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"maximum_height\": " + maxHeight + ",");
        System.out.println("    \"time_to_maximum_height\": " + timeToTop + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
