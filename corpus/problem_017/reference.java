public class problem_017 {

    public static void main(String[] args) {
        // Rocket ascent under constant acceleration; engine force = m*(a + g).
        double mass = 40;
        double a = 15;
        double t = 6;
        double g = 9.8;

        double finalVelocity = a * t;
        double distance = 0.5 * a * t * t;
        double engineForce = mass * (a + g);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_017\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"final_velocity\": " + finalVelocity + ",");
        System.out.println("    \"distance_covered\": " + distance + ",");
        System.out.println("    \"engine_force\": " + engineForce + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
