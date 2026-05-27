public class problem_008 {

    public static void main(String[] args) {
        // Average acceleration per segment: a = (v_final - v_initial) / dt.
        double a1 = (8 - 2) / 2.0;
        double a2 = (8 - 8) / 2.0;
        double a3 = (4 - 8) / 2.0;

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_008\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"acceleration_segment_1\": " + a1 + ",");
        System.out.println("    \"acceleration_segment_2\": " + a2 + ",");
        System.out.println("    \"acceleration_segment_3\": " + a3 + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
