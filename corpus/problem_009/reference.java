public class problem_009 {

    public static void main(String[] args) {
        // Braking under constant acceleration.
        double v0 = 80 / 3.6;
        double a = -3;
        double t = 6;

        double finalVelocity = v0 + a * t;
        double distance = v0 * t + 0.5 * a * t * t;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_009\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"final_velocity\": " + finalVelocity + ",");
        System.out.println("    \"distance_covered\": " + distance + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
