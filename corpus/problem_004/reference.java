public class problem_004 {

    public static void main(String[] args) {
        // From the orbital period of Phobos, recover the mass of Mars; then surface gravity.
        double G = 6.67e-11;
        double period = 7 * 3600 + 39 * 60 + 14;
        double r = 9.377e6;
        double radiusMars = 3.390e6;

        double massMars = 4 * Math.PI * Math.PI * r * r * r / (G * period * period);
        double surfaceGravity = G * massMars / (radiusMars * radiusMars);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_004\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"mass_of_mars\": " + massMars + ",");
        System.out.println("    \"surface_gravity_mars\": " + surfaceGravity + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
