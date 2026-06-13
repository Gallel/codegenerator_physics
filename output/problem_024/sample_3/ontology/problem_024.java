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
        double v_ball_relative_ice_return_speed = 21.5; // VelocityQuantity
        double neg_one = -1.0; // DimensionlessQuantity

        // --- Main Execution Flow ---
        double v_ball_relative_ice_return = neg_one * v_ball_relative_ice_return_speed;
        double v_zipi_after_throw = compute_thrower_velocity_from_ball_velocity(m_zipi, m_ball, v_ball_relative_ice_initial, neg_one);
        double v_zipi_final = compute_catch_velocity(m_zipi, m_ball, v_ball_relative_ice_return, v_zipi_after_throw);
        // --- Output Results in JSON format ---
        System.out.println("{");
        System.out.println("  \"problem\": \"problem_024\",");
        System.out.println("  \"results\": {");
        System.out.println("    \"v_zipi_final\": " + v_zipi_final + "");
        System.out.println("  }");
        System.out.println("}");
    }

    /** Conservation of momentum for a thrower-ball subsystem initially at rest: m_thrower*v_thrower + m_ball*v_ball = 0, so v_thrower = -(m_ball*v_ball)/m_thrower. */
    public static double compute_thrower_velocity_from_ball_velocity(double m_thrower, double m_ball, double v_ball, double neg_one) {
        double ball_momentum = m_ball * v_ball;
        double negative_ball_momentum = neg_one * ball_momentum;
        double v_thrower = negative_ball_momentum / m_thrower;
        return v_thrower;
    }

    /** Conservation of momentum for an inelastic catch: m_ball*v_ball + m_person*v_person_initial = (m_person + m_ball)*v_final. */
    public static double compute_catch_velocity(double m_person, double m_ball, double v_ball, double v_person_initial) {
        double ball_momentum = m_ball * v_ball;
        double person_momentum = m_person * v_person_initial;
        double total_momentum = ball_momentum + person_momentum;
        double combined_mass = m_person + m_ball;
        double v_final = total_momentum / combined_mass;
        return v_final;
    }

}