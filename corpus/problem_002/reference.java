public class problem_002 {

    public static void main(String[] args) {
        // Satellite in circular orbit. r = R_earth + altitude.
        double G = 6.67e-11;
        double massEarth = 5.972e24;
        double mass = 2000;
        double r = 6370e3 + 36000e3;
        double rSurface = 6370e3;

        double orbitalVelocity = Math.sqrt(G * massEarth / r);
        double orbitalPeriod = 2 * Math.PI * r / orbitalVelocity;
        // Energy to reach orbit = E_orbit - E_surface (kinetic at launch neglected).
        double energyOrbit = -G * massEarth * mass / (2 * r);
        double energySurface = -G * massEarth * mass / rSurface;
        double orbitalEnergyRequired = energyOrbit - energySurface;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_002\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"orbital_energy_required\": " + orbitalEnergyRequired + ",");
        System.out.println("    \"orbital_velocity\": " + orbitalVelocity + ",");
        System.out.println("    \"orbital_period\": " + orbitalPeriod + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
