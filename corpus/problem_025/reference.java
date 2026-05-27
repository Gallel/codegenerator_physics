public class problem_025 {

    public static void main(String[] args) {
        // Average force = change of momentum / time.
        double mass = 0.080;
        double v = 0.6;
        double t = 0.16;

        double averageForce = mass * v / t;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_025\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"average_force\": " + averageForce + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
