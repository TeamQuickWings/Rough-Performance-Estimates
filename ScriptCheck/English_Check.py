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

        self.assertTrue((10 ** (-5)) > error)

    def test_get_thrust_required_at_target_cruise_velocity(self):

        error = (self.a.get_thrust_required_at_target_cruise_velocity() - 278.452485) / 278.452485

        if error < 0:

            error = error * -1

        self.assertTrue((10 ** (-5)) > error)

    def test_get_target_cruise_velocity(self):

        self.assertTrue(122, self.a.get_target_cruise_velocity())

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

        print(error)

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
