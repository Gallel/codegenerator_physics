public class problem_023 {

    public static void main(String[] args) {
        // Double-acting pneumatic cylinder.
        double pistonDiameter = 0.070;
        double rodDiameter = 0.025;
        double stroke = 0.100;
        double pressure = 6e5;

        double pistonArea = Math.PI * pistonDiameter * pistonDiameter / 4;
        double rodArea = Math.PI * rodDiameter * rodDiameter / 4;
        double annularArea = pistonArea - rodArea;
        double advanceForce = pressure * pistonArea;
        double returnForce = pressure * annularArea;
        double volumeAdvance = pistonArea * stroke * 1000;
        double volumeReturn = annularArea * stroke * 1000;
        double totalVolume = volumeAdvance + volumeReturn;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_023\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"advance_force\": " + advanceForce + ",");
        System.out.println("    \"return_force\": " + returnForce + ",");
        System.out.println("    \"air_volume_advance\": " + volumeAdvance + ",");
        System.out.println("    \"air_volume_return\": " + volumeReturn + ",");
        System.out.println("    \"total_air_volume_cycle\": " + totalVolume + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
