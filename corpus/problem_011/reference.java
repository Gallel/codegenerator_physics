public class problem_011 {

    public static void main(String[] args) {
        // Uniform acceleration from rest.
        double vFinal = 108 / 3.6;
        double t = 10;

        double acceleration = vFinal / t;
        double distance = 0.5 * acceleration * t * t;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_011\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"acceleration\": " + acceleration + ",");
        System.out.println("    \"distance_covered\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
