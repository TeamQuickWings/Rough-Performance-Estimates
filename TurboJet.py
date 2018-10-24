# Andrew Scherping
# Abstract class to represent a plane and its estimated performance characteristics
# "TurboJet" is class to represent and model the performance of an aircraft with a turbojet or a turbofan
# September 2018
# Last update October 2018
# If there is a '!' please read the comment and make sure the data is filled out properly

import Plane
import math
import AirDensity
import XFLR5Data


class TurboJetEnglish1(Plane.PlaneEnglish):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_weight, cargo_weight,
                 fuel_weight, empty_weight_friction, span_efficiency_factor, thrust_specific_fuel_consumption,
                 engine_thrust, n_structure):

        name = "AirFoils/" + filename
        data = XFLR5Data.XFLR5Data(name)

        self._thrust_specific_fuel_consumption = thrust_specific_fuel_consumption * (8.6335972 * (10 ** -5))
        # conversion from lbm/(lbf*hr) to slugs/(lbf*s)
        self._aircraft_weight = aircraft_weight
        self._cargo_weight = cargo_weight
        self._fuel_weight = fuel_weight
        self._air_density = AirDensity.get_air_density_english(cruise_alt)
        self._engine_thrust = engine_thrust

        super().__init__(plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt, angle_of_attack_at_cruise,
                         target_cruise_velocity, max_velocity, aircraft_weight, cargo_weight, fuel_weight,
                         empty_weight_friction, span_efficiency_factor, n_structure, data.get_alpha_list(),
                         data.get_cl_list(), data.get_cd_list())

    def type_of_power_plant(self):

        return "Turbojet"

    def get_max_range_nm(self):

        return (2 / self._thrust_specific_fuel_consumption) * ((2 / (self._air_density * self.get_wing_area())) ** .5) \
               * (0.75 * ((1 / (3 * self.get_K() * (self.get_cD0() ** 3))) ** 0.25)) \
               * ((self.get_gross_takeoff_weight() ** 0.5) - (self.get_empty_weight() ** 0.5)) * 0.0001645788

    def get_velocity_for_max_range_knots(self):

        return (((2 / self._air_density) * self.get_wing_loading() * ((self.get_K() / (3 * self.get_cD0())) ** 0.5))
                ** 0.5) / 1.687811

    def get_max_endurance_min(self):

        return ((1 / self._thrust_specific_fuel_consumption) * ((1 / (4 * self.get_K() * self.get_cD0())) ** 0.5)
                * math.log(self.get_gross_takeoff_weight() / self.get_empty_weight(), 10)) / 60

    def get_velocity_for_max_endurance_knots(self):

        return (((2 / self._air_density) * self.get_wing_loading() * ((self.get_K() / self.get_cD0()) ** 0.5))
                ** 0.5) / 1.687811

    def get_max_rate_of_climb_ft_per_s(self):

        clcd_max = (1 / (4 * self.get_K() * self.get_cD0()))
        z = 1 + ((1 + (3 / ((clcd_max ** 2) * ((self._engine_thrust / self.get_gross_takeoff_weight()) ** 2)))) ** 0.5)
        t_w = self._engine_thrust / self.get_gross_takeoff_weight()

        return (((self.get_wing_loading() * z) / (3 * self._air_density * self.get_cD0())) ** 0.5) * \
               (t_w ** 1.5) * (1 - (z / 6) - (3 / (2 * (t_w ** 2) * (clcd_max ** 2) * z)))

    def get_velocity_for_max_rate_of_climb_knots(self):

        cl_max = (1 / (4 * self.get_K() * self.get_cD0()))
        z = 1 + ((1 + (3 / ((cl_max ** 2) * ((self._engine_thrust / self.get_gross_takeoff_weight()) ** 2)))) ** 0.5)
        t_w = self._engine_thrust / self.get_gross_takeoff_weight()

        return ((((t_w * self.get_gross_takeoff_weight()) / (3 * self._air_density * self.get_cD0())) *
                (1 + ((1 + (3 / ((cl_max ** 2) * (t_w ** 2)))) ** .5))) ** 0.5) / 1.687811

    def get_angle_of_max_rate_of_climb_in_degrees(self):

        return math.degrees(math.atan(self.get_max_rate_of_climb_ft_per_s() /
                                      self.get_velocity_for_max_rate_of_climb_knots()))


class TurboJetEnglish2(Plane.PlaneEnglish):

    def __init__(self, filename):

        # Using the "XFLRData" class to extract data from a XFLR5 text file
        location = "AirFoils/" + filename
        data = XFLR5Data.XFLR5DataEnglishJet(location)

        name = filename
        if ".txt" in filename:
            name = name[:-3]

        self._plane = TurboJetEnglish1(filename, name, data.get_wingspan(), data.get_chord(), data.get_swept_angle(),
                                       data.get_cruise_altitude(), data.get_angle_of_attack_at_cruise(),
                                       data.get_target_cruise_velocity(), data.get_max_velocity(),
                                       data.get_aircraft_weight(), data.get_cargo_weight(), data.get_fuel_weight(),
                                       data.get_cD0(), data.get_span_efficiency_factor(),
                                       data.get_thrust_specific_fuel_consumption(), data.get_engine_thrust(),
                                       data.get_n_structure())

        super().__init__(name, data.get_wingspan(), data.get_chord(), data.get_swept_angle(),
                         data.get_cruise_altitude(), data.get_angle_of_attack_at_cruise(),
                         data.get_target_cruise_velocity(), data.get_max_velocity(), data.get_aircraft_weight(),
                         data.get_cargo_weight(), data.get_fuel_weight(), data.get_cD0(),
                         data.get_span_efficiency_factor(), data.get_n_structure(), data.get_alpha_list(),
                         data.get_cl_list(), data.get_cd_list())

    def type_of_power_plant(self):

        return self._plane.type_of_power_plant()

    def get_max_range_nm(self):

        return self._plane.get_max_range_nm()

    def get_velocity_for_max_range_knots(self):

        return self._plane.get_velocity_for_max_range_knots()

    def get_max_endurance_min(self):

        return self._plane.get_max_endurance_min()

    def get_velocity_for_max_endurance_knots(self):

        return self._plane.get_velocity_for_max_range_knots()

    def get_max_rate_of_climb_ft_per_s(self):

        return self._plane.get_max_rate_of_climb_ft_per_s()

    def get_velocity_for_max_rate_of_climb_knots(self):

        return self._plane.get_velocity_for_max_rate_of_climb_knots()

    def get_angle_of_max_rate_of_climb_in_degrees(self):

        return self._plane.get_angle_of_max_rate_of_climb_in_degrees()


class TurboJetMetric1(Plane.PlaneMetric):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass, fuel_mass,
                 empty_weight_friction, span_efficiency_factor, thrust_specific_fuel_consumption,
                 engine_thrust, n_structure):

        name = "AirFoils/" + filename
        data = XFLR5Data.XFLR5Data(name)

        self._thrust_specific_fuel_consumption = thrust_specific_fuel_consumption
        self._aircraft_mass = aircraft_mass
        self._cargo_mass = cargo_mass
        self._fuel_mass = fuel_mass
        self._air_density = self._air_density = AirDensity.get_air_density_metric(cruise_alt)
        self._engine_thrust = engine_thrust
        self._gravity = 9.81

        super().__init__(plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
                         angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass,
                         fuel_mass, empty_weight_friction, span_efficiency_factor, n_structure, data.get_alpha_list(),
                         data.get_cl_list(), data.get_cd_list())

    def type_of_power_plant(self):

        return "Turbojet"

    def get_max_range(self):

        return (2 / self._thrust_specific_fuel_consumption) * ((2 / (self._air_density * self.get_wing_area())) ** .5) \
               * (0.75 * ((1 / (3 * self.get_K() * (self.get_cD0() ** 3))) ** 0.25)) \
               * ((self.get_gross_takeoff_weight() ** 0.5) - (self.get_empty_weight() ** 0.5))

    def get_velocity_for_max_range(self):

        return ((2 / self._air_density) * self.get_wing_loading() * ((self.get_K() / (3 * self.get_cD0())) ** 0.5)) \
               ** 0.5

    def get_max_endurance(self):

        return (1 / self._thrust_specific_fuel_consumption) * ((1 / (4 * self.get_K() * self.get_cD0())) ** 0.5) \
               * math.log(self.get_gross_takeoff_weight() / self.get_empty_weight(), 10)

    def get_velocity_for_max_endurance(self):

        return ((2 / self._air_density) * self.get_wing_loading() * ((self.get_K() / self.get_cD0()) ** 0.5)) \
               ** 0.5

    def get_max_rate_of_climb(self):

        clcd_max = (1 / (4 * self.get_K() * self.get_cD0()))
        z = 1 + ((1 + (3 / ((clcd_max ** 2) * ((self._engine_thrust / self.get_gross_takeoff_weight()) ** 2)))) ** 0.5)
        t_w = self._engine_thrust / self.get_gross_takeoff_weight()

        return (((self.get_wing_loading() * z) / (3 * self._air_density * self.get_cD0())) ** 0.5) * \
               (t_w ** 1.5) * (1 - (z / 6) - (3 / (2 * (t_w ** 2) * (clcd_max ** 2) * z)))

    def get_velocity_for_max_rate_of_climb(self):

        cl_max = (1 / (4 * self.get_K() * self.get_cD0()))
        z = 1 + ((1 + (3 / ((cl_max ** 2) * ((self._engine_thrust / self.get_gross_takeoff_weight()) ** 2)))) ** 0.5)
        t_w = self._engine_thrust / self.get_gross_takeoff_weight()

        return (((t_w * self.get_gross_takeoff_weight()) / (3 * self._air_density * self.get_cD0())) *
                (1 + ((1 + (3 / ((cl_max ** 2) * (t_w ** 2)))) ** .5))) ** 0.5

    def get_angle_of_max_rate_of_climb_in_degrees(self):

        return math.degrees(math.atan(self.get_max_rate_of_climb() / self.get_velocity_for_max_rate_of_climb()))


class TurboJetMetric2(Plane.PlaneMetric):

    def __init__(self, filename):

        # Using the "XFLRData" class to extract data from a XFLR5 text file
        location = "AirFoils/" + filename
        data = XFLR5Data.XFLR5DataMetricJet(location)

        name = filename
        if ".txt" in filename:
            name = name[:-3]

        self._plane = TurboJetMetric1(filename, name, data.get_wingspan(), data.get_chord(), data.get_swept_angle(),
                                      data.get_cruise_altitude(), data.get_angle_of_attack_at_cruise(),
                                      data.get_target_cruise_velocity(), data.get_max_velocity(),
                                      data.get_aircraft_mass(), data.get_cargo_mass(), data.get_fuel_mass(),
                                      data.get_cD0(), data.get_span_efficiency_factor(),
                                      data.get_thrust_specific_fuel_consumption(), data.get_engine_thrust(),
                                      data.get_n_structure())

        super().__init__(name, data.get_wingspan(), data.get_chord(), data.get_swept_angle(),
                         data.get_cruise_altitude(), data.get_angle_of_attack_at_cruise(),
                         data.get_target_cruise_velocity(), data.get_max_velocity(), data.get_aircraft_mass(),
                         data.get_cargo_mass(), data.get_fuel_mass(), data.get_cD0(),
                         data.get_span_efficiency_factor(), data.get_n_structure(), data.get_alpha_list(),
                         data.get_cl_list(), data.get_cd_list())

    def type_of_power_plant(self):

        return self._plane.type_of_power_plant()

    def get_max_range(self):

        return self._plane.get_max_range()

    def get_velocity_for_max_range(self):

        return self._plane.get_velocity_for_max_range()

    def get_max_endurance(self):

        return self._plane.get_max_endurance()

    def get_velocity_for_max_endurance(self):

        return self._plane.get_velocity_for_max_endurance()

    def get_max_rate_of_climb(self):

        return self._plane.get_max_rate_of_climb()

    def get_velocity_for_max_rate_of_climb(self):

        return self._plane.get_velocity_for_max_rate_of_climb()

    def get_angle_of_max_rate_of_climb_in_degrees(self):

        return self._plane.get_angle_of_max_rate_of_climb_in_degrees()

