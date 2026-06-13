/**
 * Generated Physics-Validated Program: problem_024
 * Automatically generated from Modular DSL.
 */
public class problem_024 {

    public static void main(String[] args) {
        // --- Main Declarations ---
        double m_zipi = 50.0; // MassQuantity
        double m_ball = 0.2; // MassQuantity
        double v_ball_relative_ice_initial_throw = 21.5; // VelocityQuantity
        double v_ball_relative_ice_return_throw_magnitude = 21.5; // VelocityQuantity
        double zero = 0.0; // DimensionlessQuantity
        double neg_one = -1.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_zipi_after_first_throw = zipi_initial_throw_velocity(m_zipi, m_ball, v_ball_relative_ice_initial_throw, zero);
        double v_ball_return = neg_one * v_ball_relative_ice_return_throw_magnitude;
        double v_zipi_final_after_catch = zipi_final_velocity_after_catch(m_zipi, m_ball, v_zipi_after_first_throw, v_ball_return);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_024\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_zipi_final_after_catch\": " + v_zipi_final_after_catch + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply conservation of linear momentum to the Zipi+ball system for the initial throw from rest. */
    public static double zipi_initial_throw_velocity(double m_zipi, double m_ball, double v_ball, double zero) {
        double ball_momentum = m_ball * v_ball;
        double negative_ball_momentum = zero - ball_momentum;
        double v_zipi_after_first_throw = negative_ball_momentum / m_zipi;
        return v_zipi_after_first_throw;
    }

    /** Apply conservation of linear momentum to the Zipi+ball system during the final catch so both move together afterward. */
    public static double zipi_final_velocity_after_catch(double m_zipi, double m_ball, double v_zipi_before_catch, double v_ball_return) {
        double zipi_momentum_before_catch = m_zipi * v_zipi_before_catch;
        double ball_momentum_before_catch = m_ball * v_ball_return;
        double total_momentum_before_catch = zipi_momentum_before_catch + ball_momentum_before_catch;
        double combined_mass_after_catch = m_zipi + m_ball;
        double v_zipi_final_after_catch = total_momentum_before_catch / combined_mass_after_catch;
        return v_zipi_final_after_catch;
    }

}