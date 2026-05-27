public class problem_007 {

    public static void main(String[] args) {
        // Spacecraft orbiting the Moon at 5 lunar radii.
        double G = 6.67e-11;
        double massMoon = 7.35e22;
        double radiusMoon = 1740e3;
        double mass = 5000;
        double r = 5 * radiusMoon;

        double orbitalVelocity = Math.sqrt(G * massMoon / r);
        double orbitalPeriod = 2 * Math.PI * r / orbitalVelocity;
        double orbitalPeriodHours = orbitalPeriod / 3600;
        double mechanicalEnergy = -G * massMoon * mass / (2 * r);
        double escapeVelocity = Math.sqrt(2 * G * massMoon / radiusMoon);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_007\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"orbital_period\": " + orbitalPeriodHours + ",");
        System.out.println("    \"mechanical_energy\": " + mechanicalEnergy + ",");
        System.out.println("    \"lunar_escape_velocity\": " + escapeVelocity + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
