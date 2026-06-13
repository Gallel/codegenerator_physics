/**
 * Generated Physics-Validated Program: problem_024
 * Automatically generated from Modular DSL.
 */
public class problem_024 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m_zipi = 50.0; // MassQuantity
        double m_zape = 50.0; // MassQuantity
        double m_ball = 0.2; // MassQuantity
        double v_ball_relative_ice_initial = 21.5; // VelocityQuantity
        double v_ball_relative_ice_return = 21.5; // VelocityQuantity
        double zero = 0.0; // DimensionlessQuantity
        double neg_one = -1.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_zipi_after_throw = zipi_throw_velocity(m_zipi, m_ball, v_ball_relative_ice_initial, neg_one);
        double v_zape_with_ball = zape_catch_velocity(m_zape, m_ball, v_ball_relative_ice_initial);
        double v_zape_after_throw = zape_throw_back_velocity(m_zape, m_ball, v_zape_with_ball, v_ball_relative_ice_return, neg_one);
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

    /** Apply conservation of linear momentum to Zape catching the incoming ball: m_ball*v_ball = (m_zape+m_ball)*v_zape_with_ball. */
    public static double zape_catch_velocity(double m_zape, double m_ball, double v_ball) {
        double incoming_ball_momentum = m_ball * v_ball;
        double combined_mass = m_zape + m_ball;
        double v_zape_with_ball = incoming_ball_momentum / combined_mass;
        return v_zape_with_ball;
    }

    /** Apply conservation of linear momentum to Zape throwing the ball back: (m_zape+m_ball)*v_before = m_zape*v_zape_after_throw + m_ball*(-v_ball_return). */
    public static double zape_throw_back_velocity(double m_zape, double m_ball, double v_zape_with_ball, double v_ball_return, double neg_one) {
        double combined_mass = m_zape + m_ball;
        double initial_system_momentum = combined_mass * v_zape_with_ball;
        double v_ball_return_signed = neg_one * v_ball_return;
        double returned_ball_momentum = m_ball * v_ball_return_signed;
        double zape_momentum_after_throw = initial_system_momentum - returned_ball_momentum;
        double v_zape_after_throw = zape_momentum_after_throw / m_zape;
        return v_zape_after_throw;
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