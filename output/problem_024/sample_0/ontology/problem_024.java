/**
 * Generated Physics-Validated Program: problem_024
 * Automatically generated from Modular DSL.
 */
public class problem_024 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m_zipi = 50.0; // MassQuantity
        double m_ball = 0.2; // MassQuantity
        double v_ball_relative_ice_initial = 21.5; // VelocityQuantity
        double v_ball_relative_ice_return = 21.5; // VelocityQuantity
        double neg_one = -1.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_zipi_after_throw = zipi_throw_velocity(m_zipi, m_ball, v_ball_relative_ice_initial, neg_one);
        double v_zipi_final = zipi_final_catch_velocity(m_zipi, m_ball, v_zipi_after_throw, v_ball_relative_ice_return, neg_one);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_024\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_zipi_final\": " + v_zipi_final + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply conservation of linear momentum to Zipi throwing the ball from rest: m_zipi*v_zipi_after_throw + m_ball*v_ball = 0. */
    public static double zipi_throw_velocity(double m_zipi, double m_ball, double v_ball, double neg_one) {
        double ball_momentum = m_ball * v_ball;
        double opposite_momentum = neg_one * ball_momentum;
        double v_zipi_after_throw = opposite_momentum / m_zipi;
        return v_zipi_after_throw;
    }

    /** Apply conservation of linear momentum to Zipi catching the returned ball: m_zipi*v_zipi_after_throw + m_ball*(-v_ball_return) = (m_zipi+m_ball)*v_zipi_final. */
    public static double zipi_final_catch_velocity(double m_zipi, double m_ball, double v_zipi_after_throw, double v_ball_return, double neg_one) {
        double zipi_momentum_before_catch = m_zipi * v_zipi_after_throw;
        double v_ball_return_signed = neg_one * v_ball_return;
        double ball_momentum_before_catch = m_ball * v_ball_return_signed;
        double total_momentum_before_catch = zipi_momentum_before_catch + ball_momentum_before_catch;
        double combined_mass_after_catch = m_zipi + m_ball;
        double v_zipi_final = total_momentum_before_catch / combined_mass_after_catch;
        return v_zipi_final;
    }

}