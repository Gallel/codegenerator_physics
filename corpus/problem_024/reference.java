public class problem_024 {

    public static void main(String[] args) {
        // Momentum conservation. Zipi recoils when throwing, then catches the returning ball.
        double massPerson = 50;
        double massBall = 0.200;
        double ballSpeed = 21.5;

        // After throwing: 0 = massPerson*vZipi + massBall*ballSpeed
        double vAfterThrow = -massBall * ballSpeed / massPerson;
        // After catching the ball coming back (towards Zipi, opposite sign):
        double momentumBefore = massPerson * vAfterThrow + massBall * (-ballSpeed);
        double finalVelocity = momentumBefore / (massPerson + massBall);
        finalVelocity = Math.abs(finalVelocity);

        System.out.println("{");
        System.out.println("  \"problem\": \"problem_024\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"final_velocity_zipi\": " + finalVelocity + "");
        System.out.println("  }");
        System.out.println("}");
    }
}
