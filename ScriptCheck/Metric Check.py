import PistonEngine
import unittest


class TestPlane(unittest.TestCase):

    def setUp(self):

        self.a = PistonEngine.PistonEngineMetric2("Cessna172Metric.txt")

    def test_get_wingspan(self):

        self.assertEqual(11, self.a.get_wing_span())

    def test_get_gross_takeoff_weight(self):

        self.assertEqual(10898.91, self.a.get_gross_takeoff_weight())

    def test_get_empty_weight(self):

        self.assertEqual(9221.4, self.a.get_empty_weight())

    def test_get_power_required_at_target_cruise_velocity(self):

        error = (self.a.get_power_required_at_target_cruise_velocity() - 76794.3385) / 76794.3385

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_thrust_required_at_target_cruise_velocity(self):

        error = (self.a.get_thrust_required_at_target_cruise_velocity() - 1238.61836) / 1238.61836

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_target_cruise_velocity(self):

        self.assertTrue(62, self.a.get_target_cruise_velocity())

    def test_get_k(self):

        error = (self.a.get_k() - 0.056965) / 0.056965

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_K(self):

        error = (self.a.get_K() - 0.0491635) / 0.0491635

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    # TODO
    def test_get_cL_at_cruise(self):

        return None

    # TODO
    def test_get_cD_at_cruise(self):

        return None

    def test_get_wing_loading(self):

        error = (self.a.get_wing_loading() - 719.020319) / 719.020319

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_cD0(self):

        self.assertEqual(0.0341, self.a.get_cD0())

    def test_get_wing_area(self):

        error = (self.a.get_wing_area() - 15.158) / 15.158

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_cL_max(self):

        error = (self.a.get_cL_max() - 1.1558696) / 1.1558696

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_v_stall_at_cruise(self):

        error = (self.a.get_v_stall_at_cruise() - 34.330039) / 34.330039

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_v_stall_at_sea_level(self):

        error = (self.a.get_v_stall_at_sea_level() - 31.86861) / 31.86861

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

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

        error = (self.a.get_maneuvering_velocity() - 84.091079) / 84.091079

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    # TODO
    def test_turn_rate_at_maneuvering_velocity(self):

        error = (self.a.get_turn_rate_at_maneuvering_velocity() - 39.543557) / 39.543557

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    # TODO
    def test_get_pull_up_radius_at_target_velocity(self):

        return None

    # TODO
    def test_get_pull_up_rate_at_target_velocity(self):

        return None

    def test_get_min_pull_up_radius(self):

        error = (self.a.get_min_pull_up_radius() - 144.1653342) / 144.1653342

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_max_pull_up_rate(self):

        error = (self.a.get_max_pull_up_rate() - 33.4204056) / 33.4204056

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)


class TestPistonEngine(unittest.TestCase):

    def setUp(self):

        self.a = PistonEngine.PistonEngineMetric2("Cessna172Metric.txt")

    def test_get_max_range(self):

        error = (self.a.get_max_range() - 1138484.190046685) / 1138484.190046685

        print(self.a.get_max_range())

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_velocity_for_max_range(self):

        error = (self.a.get_velocity_for_max_range() - 40.4436964) / 40.4436964

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    # TODO
    def test_get_max_endurance(self):

        return None

    # TODO
    def test_fet_velocity_for_max_endurance(self):

        return None

    def test_get_rate_of_climb_at_cruise(self):

        error = (self.a.get_rate_of_climb_at_cruise() - 3.594389) / 3.594389

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_velocity_for_rate_of_climb_at_cruise(self):

        error = (self.a.get_velocity_for_rate_of_climb_at_cruise() - 34.330039) / 34.330039

        print(error)

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_angle_of_climb_at_cruise_in_degrees(self):

        error = (self.a.get_angle_of_climb_at_cruise_in_degrees() - 5.977147) / 5.977147

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_max_rate_of_climb(self):

        error = (self.a.get_max_rate_of_climb() - 5.0090187) / 5.0090187

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_velocity_for_max_rate_of_climb(self):

        error = (self.a.get_velocity_for_max_rate_of_climb() - 31.86861) / 31.86861

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_angle_of_max_rate_of_climb_in_degrees(self):

        error = (self.a.get_angle_of_max_rate_of_climb_in_degrees() - 8.93251) / 8.93251

        if error < 0:
            error = error * -1

        self.assertTrue((10 ** (-5)) > error)
