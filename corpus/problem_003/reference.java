public class problem_003 {

    public static void main(String[] args) {
        // Moon in circular orbit around the Earth.
        double G = 6.67e-11;
        double massEarth = 5.972e24;
        double r = 3.84e8;

        double orbitalVelocity = Math.sqrt(G * massEarth / r);
        double orbitalPeriod = 2 * Math.PI * r / orbitalVelocity;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_003\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"orbital_velocity\": " + orbitalVelocity + ",");
        System.out.println("    \"orbital_period\": " + orbitalPeriod + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
