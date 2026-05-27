public class problem_005 {

    public static void main(String[] args) {
        // Didymos: mass from density and sphere volume, then surface gravity and force on Dimorphos.
        double G = 6.67e-11;
        double diameter = 781;
        double density = 2146;
        double radius = diameter / 2;
        double massDimorphos = 4.42e10;
        double distance = 1120;

        double volume = (4.0 / 3.0) * Math.PI * radius * radius * radius;
        double massDidymos = density * volume;
        double surfaceGravity = G * massDidymos / (radius * radius);
        double gravForce = G * massDidymos * massDimorphos / (distance * distance);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_005\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"mass_of_didymos\": " + massDidymos + ",");
        System.out.println("    \"surface_gravity_didymos\": " + surfaceGravity + ",");
        System.out.println("    \"gravitational_force_on_dimorphos\": " + gravForce + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
