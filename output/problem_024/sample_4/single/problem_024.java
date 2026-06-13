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
        double v_ball_relative_ice_initial_throw = 21.5; // VelocityQuantity
        double v_ball_relative_ice_return_throw = 21.5; // VelocityQuantity
        double zero_velocity = 0.0; // VelocityQuantity
        int negative_one = -1; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_zipi_after_throw = compute_zipi_after_throw(m_zipi, m_ball, v_ball_relative_ice_initial_throw, zero_velocity);
        double v_zape_with_ball_after_catch = compute_zape_with_ball_after_catch(m_zape, m_ball, v_ball_relative_ice_initial_throw);
        double v_ball_return_signed = negative_one * v_ball_relative_ice_return_throw;
        double v_zape_after_return_throw = compute_zape_after_return_throw(m_zape, m_ball, v_zape_with_ball_after_catch, v_ball_return_signed);
        double v_zipi_final = compute_zipi_final_after_catch(m_zipi, m_ball, v_zipi_after_throw, v_ball_return_signed);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_024\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_zipi_final\": " + v_zipi_final + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply conservation of momentum to Zipi and the ball during the first throw: initial momentum zero equals final momentum of Zipi plus ball. */
    public static double compute_zipi_after_throw(double m_zipi, double m_ball, double v_ball_initial, double zero_velocity) {
        double ball_momentum_initial = m_ball * v_ball_initial;
        double zipi_momentum_after_throw = zero_velocity - ball_momentum_initial;
        double v_zipi_after_throw = zipi_momentum_after_throw / m_zipi;
        return v_zipi_after_throw;
    }

    /** Apply conservation of momentum to Zape and the incoming ball during the catch so they move together afterward. */
    public static double compute_zape_with_ball_after_catch(double m_zape, double m_ball, double v_ball_initial) {
        double incoming_ball_momentum = m_ball * v_ball_initial;
        double combined_mass = m_zape + m_ball;
        double v_zape_with_ball_after_catch = incoming_ball_momentum / combined_mass;
        return v_zape_with_ball_after_catch;
    }

    /** Apply conservation of momentum to Zape and the ball during the return throw, with the ball leaving toward Zipi. */
    public static double compute_zape_after_return_throw(double m_zape, double m_ball, double v_zape_with_ball_after_catch, double v_ball_return_signed) {
        double combined_mass = m_zape + m_ball;
        double momentum_before_return_throw = combined_mass * v_zape_with_ball_after_catch;
        double ball_momentum_after_return_throw = m_ball * v_ball_return_signed;
        double zape_momentum_after_return_throw = momentum_before_return_throw - ball_momentum_after_return_throw;
        double v_zape_after_return_throw = zape_momentum_after_return_throw / m_zape;
        return v_zape_after_return_throw;
    }

    /** Apply conservation of momentum to Zipi and the returned ball during the final catch so they move together afterward. */
    public static double compute_zipi_final_after_catch(double m_zipi, double m_ball, double v_zipi_after_throw, double v_ball_return_signed) {
        double zipi_momentum_before_final_catch = m_zipi * v_zipi_after_throw;
        double ball_momentum_before_final_catch = m_ball * v_ball_return_signed;
        double total_momentum_before_final_catch = zipi_momentum_before_final_catch + ball_momentum_before_final_catch;
        double zipi_ball_combined_mass = m_zipi + m_ball;
        double v_zipi_final = total_momentum_before_final_catch / zipi_ball_combined_mass;
        return v_zipi_final;
    }

}