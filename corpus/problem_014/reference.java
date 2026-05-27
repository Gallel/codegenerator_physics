public class problem_014 {

    public static void main(String[] args) {
        // Uniform circular motion from frequency.
        double radius = 0.50;
        double frequency = 10;

        double period = 1 / frequency;
        double angularVelocity = 2 * Math.PI * frequency;
        double linearVelocity = angularVelocity * radius;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_014\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"period\": " + period + ",");
        System.out.println("    \"angular_velocity\": " + angularVelocity + ",");
        System.out.println("    \"linear_velocity\": " + linearVelocity + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
