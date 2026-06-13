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
        double p_system_initial = 0.0; // MomentumQuantity
        int neg_one = -1; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_zipi_after_throw = zipi_throw_velocity(p_system_initial, m_zipi, m_ball, v_ball_relative_ice_initial);
        double v_ball_after_return_throw = neg_one * v_ball_relative_ice_return;
        double v_zipi_final_after_catch = zipi_final_catch_velocity(m_zipi, m_ball, v_zipi_after_throw, v_ball_after_return_throw);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_024\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_zipi_final_after_catch\": " + v_zipi_final_after_catch + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply conservation of momentum to Zipi throwing the ball: 0 = m_zipi*v_zipi_after_throw + m_ball*v_ball_relative_ice_initial. */
    public static double zipi_throw_velocity(double p_initial, double m_zipi, double m_ball, double v_ball) {
        double p_ball = m_ball * v_ball;
        double p_zipi = p_initial - p_ball;
        double v_zipi_after_throw = p_zipi / m_zipi;
        return v_zipi_after_throw;
    }

    /** Apply conservation of momentum to Zipi catching the returning ball: m_zipi*v_zipi_before + m_ball*v_ball_return_signed = (m_zipi + m_ball)*v_zipi_final_after_catch. */
    public static double zipi_final_catch_velocity(double m_zipi, double m_ball, double v_zipi_before, double v_ball_return_signed) {
        double p_zipi_before_catch = m_zipi * v_zipi_before;
        double p_ball_before_catch = m_ball * v_ball_return_signed;
        double p_total_before_final_catch = p_zipi_before_catch + p_ball_before_catch;
        double m_zipi_ball_total = m_zipi + m_ball;
        double v_zipi_final_after_catch = p_total_before_final_catch / m_zipi_ball_total;
        return v_zipi_final_after_catch;
    }

}