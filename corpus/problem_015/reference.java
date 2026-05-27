public class problem_015 {

    public static void main(String[] args) {
        // Circular motion from angular velocity.
        double radius = 0.50;
        double angularVelocity = Math.PI / 2;

        double linearVelocity = angularVelocity * radius;
        double centripetalAcceleration = angularVelocity * angularVelocity * radius;
        double period = 2 * Math.PI / angularVelocity;
        double frequency = 1 / period;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_015\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"linear_velocity\": " + linearVelocity + ",");
        System.out.println("    \"centripetal_acceleration\": " + centripetalAcceleration + ",");
        System.out.println("    \"period\": " + period + ",");
        System.out.println("    \"frequency\": " + frequency + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
