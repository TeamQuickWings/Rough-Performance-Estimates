import PistonEngine
import unittest


class TestPlane(unittest.TestCase):

    def setUp(self):

        self.a = PistonEngine.PistonEngineEnglish2("Cessna172.txt")

    def test_get_wingspan(self):

        self.assertEqual(36.09, self.a.get_wing_span())

    def test_get_gross_takeoff_weight(self):

        self.assertEqual(2449, self.a.get_gross_takeoff_weight())

    def test_get_empty_weight(self):

        self.assertEqual(2072, self.a.get_empty_weight())

    def test_get_power_required_at_target_cruise_velocity(self):

        error = (self.a.get_power_required_at_target_cruise_velocity() - 102.982904) / 102.982904

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_thrust_required_at_target_cruise_velocity(self):

        error = (self.a.get_thrust_required_at_target_cruise_velocity() - 278.452485) / 278.452485

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_target_cruise_velocity(self):

        self.assertTrue(122, self.a.get_target_cruise_velocity())

    def test_get_k(self):

        error = (self.a.get_k() - 0.056965) / 0.056965

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-4)) > error)

    def test_get_K(self):

        error = (self.a.get_K() - 0.0491635) / 0.0491635

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-4)) > error)

    # TODO
    def test_get_cL_at_cruise(self):

        return None

    # TODO
    def test_get_cD_at_cruise(self):

        return None

    def test_get_wing_loading(self):

        error = (self.a.get_wing_loading() - 15.00954) / 15.00954

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_cD0(self):

        self.assertEqual(0.0341, self.a.get_cD0())

    def test_get_wing_area(self):

        error = (self.a.get_wing_area() - 163.16289) / 163.16289

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_cL_max(self):

        error = (self.a.get_cL_max() - 1.1558696) / 1.1558696

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_v_stall_at_cruise(self):

        error = (self.a.get_v_stall_at_cruise() - 66.732226) / 66.732226

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-3)) > error)

    def test_get_v_stall_at_sea_level(self):

        error = (self.a.get_v_stall_at_sea_level() - 61.93199) / 61.93199

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-4)) > error)

    # TODO
    def test_get_lift_force_at_target_velocity(self):

        return None

    # TODO
    def test_get_n_at_target_velocity(self):

        return None

    # TODO
    def test_get_turn_radius_at_target_velocity(self):

        return None

    # TODO
    def test_get_turn_rate_at_target_velocity(self):

        return None

    def test_get_maneuvering_velocity(self):

        error = (self.a.get_maneuvering_velocity() - 163.459939367676) / 163.459939367676

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-3)) > error)

    def test_turn_rate_at_maneuvering_velocity(self):

        error = (self.a.get_turn_rate_at_maneuvering_velocity() - 39.543557) / 39.543557

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-3)) > error)

    # TODO
    def test_get_pull_up_radius_at_target_velocity(self):

        return None

    # TODO
    def test_get_pull_up_rate_at_target_velocity(self):

        return None

    def test_get_min_pull_up_radius(self):

        error = (self.a.get_min_pull_up_radius() - 472.98338) / 472.98338

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-3)) > error)

    def test_get_max_pull_up_rate(self):

        error = (self.a.get_max_pull_up_rate() - 33.4204056) / 33.4204056

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-3)) > error)


class TestPistonEngine(unittest.TestCase):

    def setUp(self):

        self.a = PistonEngine.PistonEngineEnglish2("Cessna172.txt")

    def test_get_max_range(self):

        error = (self.a.get_max_range() - 614.7319891835662) / 614.7319891835662

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_velocity_for_max_range(self):

        # value in nautical mile
        error = (self.a.get_velocity_for_max_range() - 78.616256806809801) / 78.616256806809801

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-3)) > error)

    def test_get_max_endurance(self):

        error = (self.a.get_max_endurance() - 77050.54459) / 77050.54459

        print(error)

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_velocity_for_max_endurance(self):

        error = (self.a.get_velocity_for_max_endurance() - 59.73540855647877) / 59.73540855647877

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_rate_of_climb_at_cruise_ft_per_s(self):

        error = (self.a.get_rate_of_climb_at_cruise() - 11.792615408852265) / 11.792615408852265

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_velocity_for_rate_of_climb_at_cruise(self):

        error = (self.a.get_velocity_for_rate_of_climb_at_cruise() - 66.732257494935496) / 66.732257494935496

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_angle_of_climb_at_cruise_in_degrees(self):

        error = (self.a.get_angle_of_climb_at_cruise() - 5.977147) / 5.977147

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_max_rate_of_climb(self):

        # did nothing
        error = (self.a.get_max_rate_of_climb() - 16.66371767051391) / 16.66371767051391

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-1)) > error)

    def test_get_velocity_for_max_rate_of_climb(self):

        # units in knots knots
        error = (self.a.get_velocity_for_max_rate_of_climb() - 61.947622271145001) / 61.947622271145001

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-2)) > error)

    def test_get_angle_of_max_rate_of_climb_in_degrees(self):

        # did nothing
        error = (self.a.get_angle_of_max_rate_of_climb() - 8.932510046315384) / 8.932510046315384

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-1)) > error)
