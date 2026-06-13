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
        double p_system_initial = 0.0; // MomentumQuantity

        // --- Main Execution Flow ---
        double v_zipi_after_throw = compute_velocity_from_zero_momentum_throw(m_zipi, m_ball, v_ball_relative_ice_initial, p_system_initial);
        double v_zape_with_ball_after_catch = compute_catch_velocity(m_zape, m_ball, p_system_initial, v_ball_relative_ice_initial);
        double v_ball_after_return_throw = p_system_initial - v_ball_relative_ice_return;
        double v_zape_after_throw_back = compute_throw_back_velocity(m_zape, m_ball, v_zape_with_ball_after_catch, v_ball_after_return_throw);
        double v_zipi_final_after_catch = compute_catch_velocity(m_zipi, m_ball, v_zipi_after_throw, v_ball_after_return_throw);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_024\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_zipi_final_after_catch\": " + v_zipi_final_after_catch + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Apply conservation of momentum to a throw from rest: 0 = m_person * v_person + m_ball * v_ball, solving for the person's recoil velocity. */
    public static double compute_velocity_from_zero_momentum_throw(double m_person, double m_ball, double v_ball, double p_initial) {
        double ball_momentum = m_ball * v_ball;
        double person_momentum = p_initial - ball_momentum;
        double person_velocity = person_momentum / m_person;
        return person_velocity;
    }

    /** Apply conservation of momentum to an inelastic catch where person and ball move together after the catch. */
    public static double compute_catch_velocity(double m_person, double m_ball, double v_person_before, double v_ball_before) {
        double person_momentum_before = m_person * v_person_before;
        double ball_momentum_before = m_ball * v_ball_before;
        double total_momentum_before = person_momentum_before + ball_momentum_before;
        double combined_mass = m_person + m_ball;
        double combined_velocity_after_catch = total_momentum_before / combined_mass;
        return combined_velocity_after_catch;
    }

    /** Apply conservation of momentum to Zape throwing the ball back with opposite signed velocity. */
    public static double compute_throw_back_velocity(double m_person, double m_ball, double v_person_ball_initial, double v_ball_after_throw) {
        double initial_combined_mass = m_person + m_ball;
        double initial_total_momentum = initial_combined_mass * v_person_ball_initial;
        double ball_final_momentum = m_ball * v_ball_after_throw;
        double person_final_momentum = initial_total_momentum - ball_final_momentum;
        double person_velocity_after_throw = person_final_momentum / m_person;
        return person_velocity_after_throw;
    }

}