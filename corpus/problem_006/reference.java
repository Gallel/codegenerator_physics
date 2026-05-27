public class problem_006 {

    public static void main(String[] args) {
        // Nanosatellite in low orbit; launch speed by energy conservation.
        double G = 6.67e-11;
        double massEarth = 5.98e24;
        double radiusEarth = 6.37e6;
        double r = radiusEarth + 500e3;

        double orbitalVelocity = Math.sqrt(G * massEarth / r);
        double orbitalPeriod = 2 * Math.PI * r / orbitalVelocity;
        // 1/2 v0^2 - GM/R = 1/2 v_orb^2 - GM/r
        double v0Squared = orbitalVelocity * orbitalVelocity - 2 * G * massEarth / r + 2 * G * massEarth / radiusEarth;
        double initialVelocity = Math.sqrt(v0Squared);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_006\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"orbital_velocity\": " + orbitalVelocity + ",");
        System.out.println("    \"orbital_period\": " + orbitalPeriod + ",");
        System.out.println("    \"initial_velocity_from_surface\": " + initialVelocity + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
