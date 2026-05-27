public class problem_010 {

    public static void main(String[] args) {
        // Uniform deceleration until stop.
        double v0 = 90 / 3.6;
        double t = 5;

        double acceleration = (0 - v0) / t;
        double distance = v0 * t + 0.5 * acceleration * t * t;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_010\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"acceleration\": " + acceleration + ",");
        System.out.println("    \"distance_covered\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
