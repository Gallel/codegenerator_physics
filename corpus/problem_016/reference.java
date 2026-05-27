public class problem_016 {

    public static void main(String[] args) {
        // Spinning disk at 300 rpm; centripetal acceleration at two radii.
        double rpm = 300;
        double radiusEdge = 0.10;
        double radiusInner = 0.05;

        double frequency = rpm / 60;
        double period = 1 / frequency;
        double angularVelocity = 2 * Math.PI * frequency;
        double accEdge = angularVelocity * angularVelocity * radiusEdge;
        double accInner = angularVelocity * angularVelocity * radiusInner;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_016\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"period\": " + period + ",");
        System.out.println("    \"frequency\": " + frequency + ",");
        System.out.println("    \"centripetal_acceleration_surface\": " + accEdge + ",");
        System.out.println("    \"centripetal_acceleration_at_5_cm\": " + accInner + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
