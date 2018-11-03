# Andrew Scherping
# Abstract class to represent a plane and its estimated performance characteristics
# "PistionEngine" is class to represent and model the performance of an aircraft with a reciprocating piston engine
# or a turboprop
# September 2018
# Last update October 2018
# If there is a '!' please read the comment and make sure the data is filled out properly

import Plane
import math
import AirDensity
import XFLR5Data


class PistonEngineEnglish1(Plane.PlaneEnglish):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_weight, cargo_weight,
                 fuel_weight, empty_weight_friction, span_efficiency_factor, specific_fuel_consumption,
                 propeller_efficiency, engine_power, n_structure):

        name = "AirFoils/" + filename
        data = XFLR5Data.XFLR5Data(name)

        self._specific_fuel_consumption = specific_fuel_consumption * 5.11686929 * (10 ** (-7))  # conversion from
        # lb/(hp*hr) to lb/(((lb*ft)/s)*s)
        self._propeller_efficiency = propeller_efficiency
        self._aircraft_weight = aircraft_weight
        self._cargo_weight = cargo_weight
        self._fuel_weight = fuel_weight
        self._air_density = AirDensity.get_air_density_english(cruise_alt)
        self._engine_power = (engine_power * 32572) / 60

        super().__init__(plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt, angle_of_attack_at_cruise,
                         target_cruise_velocity, max_velocity, aircraft_weight, cargo_weight, fuel_weight,
                         empty_weight_friction, span_efficiency_factor, n_structure, data.get_alpha_list(),
                         data.get_cl_list(), data.get_cd_list())

    def type_of_power_plant(self):

        return "Piston Engine"

    def get_max_range(self):

        return ((self._propeller_efficiency / self._specific_fuel_consumption) *
                ((1 / (4 * self.get_K() * self.get_cD0())) ** .5) *
                (math.log((self.get_gross_takeoff_weight() / self.get_empty_weight()), 10))) * 0.0001645788

    def get_velocity_for_max_range(self):

        return (((2 / self._air_density) * self.get_wing_loading() * ((self.get_K() / self.get_cD0()) ** .5)) ** 0.5) \
               / 1.687811

    def get_max_endurance(self):

        return ((self._propeller_efficiency / self._specific_fuel_consumption) *
                (0.25 * ((3 / (self.get_K() * (self.get_cD0() ** (1/3)))) ** (3 / 4))) *
                ((2 * self._air_density * self._wing_area) ** 0.5) *
                ((1 / (self.get_empty_weight() ** 0.5)) - (1 / (self.get_gross_takeoff_weight() ** 0.5))))

    def get_velocity_for_max_endurance(self):

        return ((((2 / self._air_density) * self.get_wing_loading() *
                 ((self.get_K() / (3 * self.get_cD0())) ** 0.5)) ** 0.5)) / 1.687811

    def get_rate_of_climb_at_cruise(self):

        power = ((1.132 * (self._air_density / AirDensity.get_air_density_english(0))) - 0.132) * self._engine_power

        return ((self._propeller_efficiency * power) / self.get_gross_takeoff_weight()) - \
               ((((2 / self._air_density) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())
                ** 0.5) * (1.155 / ((1 / (4 * self.get_K() * self.get_cD0())) ** 0.5)))

    def get_velocity_for_rate_of_climb_at_cruise(self):

        v_climb = (((2 / self._air_density) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())
                   ** 0.5) / 1.687811

        if v_climb < self.get_v_stall_at_cruise():

            return self.get_v_stall_at_cruise()

        else:

            return v_climb

    def get_angle_of_climb_at_cruise(self):

        return math.degrees(math.atan((self.get_rate_of_climb_at_cruise() * 0.5924835) /
                                      self.get_velocity_for_rate_of_climb_at_cruise()))

    def get_max_rate_of_climb(self):

        air_density = AirDensity.get_air_density_english(0)

        return ((self._propeller_efficiency * self._engine_power) / self.get_gross_takeoff_weight()) - \
               ((((2 / air_density) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())
                ** 0.5) * (1.155 / ((1 / (4 * self.get_K() * self.get_cD0())) ** 0.5)))

    def get_velocity_for_max_rate_of_climb(self):

        air_density = AirDensity.get_air_density_english(0)

        v_climb = (((2 / air_density) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())
                   ** 0.5) / 1.687811

        if v_climb < self.get_v_stall_at_sea_level():

            return self.get_v_stall_at_sea_level()

        else:

            return v_climb

    def get_angle_of_max_rate_of_climb(self):

        return math.degrees(math.atan((self.get_max_rate_of_climb() * 0.5924835) /
                                      self.get_velocity_for_max_rate_of_climb()))


class PistonEngineEnglish2(Plane.PlaneEnglish):

    def __init__(self, filename):

        # Using the "XFLRData" class to extract data from a XFLR5 text file
        location = "AirFoils/" + filename
        data = XFLR5Data.XFLR5DataEnglishProp(location)

        name = filename
        if ".txt" in filename:
            name = name[:-4]

        self._plane = PistonEngineEnglish1(filename, name, data.get_wingspan(), data.get_chord(),
                                           data.get_swept_angle(), data.get_cruise_altitude(),
                                           data.get_angle_of_attack_at_cruise(), data.get_target_cruise_velocity(),
                                           data.get_max_velocity(), data.get_aircraft_weight(), data.get_cargo_weight(),
                                           data.get_fuel_weight(), data.get_cD0(),
                                           data.get_span_efficiency_factor(), data.get_specific_fuel_consumption(),
                                           data.get_propeller_efficiency(), data.get_engine_power(),
                                           data.get_n_structure())

        super().__init__(name, data.get_wingspan(), data.get_chord(), data.get_swept_angle(),
                         data.get_cruise_altitude(), data.get_angle_of_attack_at_cruise(),
                         data.get_target_cruise_velocity(), data.get_max_velocity(), data.get_aircraft_weight(),
                         data.get_cargo_weight(), data.get_fuel_weight(), data.get_cD0(),
                         data.get_span_efficiency_factor(), data.get_n_structure(),
                         data.get_alpha_list(), data.get_cl_list(), data.get_cd_list())

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

    def get_angle_of_max_rate_of_climb(self):

        return self._plane.get_angle_of_max_rate_of_climb()

    def get_rate_of_climb_at_cruise(self):

        return self._plane.get_rate_of_climb_at_cruise()

    def get_velocity_for_rate_of_climb_at_cruise(self):

        return self._plane.get_velocity_for_rate_of_climb_at_cruise()

    def get_angle_of_climb_at_cruise(self):

        return self._plane.get_angle_of_climb_at_cruise()


class PistonEngineMetric1(Plane.PlaneMetric):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass, fuel_mass,
                 empty_weight_friction, span_efficiency_factor, specific_fuel_consumption, propeller_efficiency,
                 engine_power, n_structure):

        name = "AirFoils/" + filename
        data = XFLR5Data.XFLR5Data(name)

        self._specific_fuel_consumption = specific_fuel_consumption * (2.725 * (10 ** (-9)))
        self._propeller_efficiency = propeller_efficiency
        self._aircraft_mass = aircraft_mass
        self._cargo_mass = cargo_mass
        self._fuel_mass = fuel_mass
        self._air_density = AirDensity.get_air_density_metric(cruise_alt)
        self._engine_power = engine_power
        self._gravity = 9.81

        super().__init__(plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt, angle_of_attack_at_cruise,
                         target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass, fuel_mass,
                         empty_weight_friction, span_efficiency_factor, n_structure, data.get_alpha_list(),
                         data.get_cl_list(), data.get_cd_list())

    def type_of_power_plant(self):

        return "Piston Engine"

    def get_max_range(self):

        return (self._propeller_efficiency / self._specific_fuel_consumption) * \
               ((1 / (4 * self.get_K() * self.get_cD0())) ** .5) * \
               (math.log((self.get_gross_takeoff_weight() / self.get_empty_weight()), 10))

    def get_velocity_for_max_range(self):

        return ((2 / self._air_density) * self.get_wing_loading() * ((self.get_K() / self.get_cD0()) ** .5)) ** 0.5

    def get_max_endurance(self):

        return (self._propeller_efficiency / self._specific_fuel_consumption) * \
               (0.25 * ((3 / (self.get_K() * (self.get_cD0() ** (1 / 3)))) ** (3 / 4))) * \
               ((2 * self._air_density * self._wing_area) ** 0.5) * \
               ((self.get_empty_weight() ** -0.5) - (self.get_gross_takeoff_weight() ** -0.5))

    def get_velocity_for_max_endurance(self):

        return (((2 / self._air_density) * self.get_wing_loading() *
                 ((self.get_K() / (3 * self.get_cD0())) ** 0.5)) ** 0.5)

    def get_rate_of_climb_at_cruise(self):

        power = (1.132 * (self._air_density / 1.225) - 0.132) * self._engine_power

        return ((self._propeller_efficiency * power) / self.get_gross_takeoff_weight()) - \
               ((((2 / self._air_density) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())
                   ** 0.5) * (1.155 / ((1 / (4 * self.get_K() * self.get_cD0())) ** 0.5)))

    def get_velocity_for_rate_of_climb_at_cruise(self):

        v_climb = ((2 / self._air_density) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())\
                  ** 0.5

        if v_climb < self.get_v_stall_at_cruise():

            return self.get_v_stall_at_cruise()

        else:

            return v_climb

    def get_angle_of_climb_at_cruise_in_degrees(self):

        return math.degrees(math.atan(self.get_rate_of_climb_at_cruise() /
                                      self.get_velocity_for_rate_of_climb_at_cruise()))

    def get_max_rate_of_climb(self):

        return ((self._propeller_efficiency * self._engine_power) / self.get_gross_takeoff_weight()) - \
               ((((2 / 1.225) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())
                 ** 0.5) * (1.155 / ((1 / (4 * self.get_K() * self.get_cD0())) ** 0.5)))

    def get_velocity_for_max_rate_of_climb(self):

        v_climb = ((2 / 1.225) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading()) ** 0.5

        if v_climb < self.get_v_stall_at_sea_level():

            return self.get_v_stall_at_sea_level()

        else:

            return v_climb

    def get_angle_of_max_rate_of_climb_in_degrees(self):

        return math.degrees(math.atan(self.get_max_rate_of_climb() / self.get_velocity_for_max_rate_of_climb()))


class PistonEngineMetric2(Plane.PlaneMetric):

    def __init__(self, filename):

        # Using the "XFLRData" class to extract data from a XFLR5 text file
        location = "AirFoils/" + filename
        data = XFLR5Data.XFLR5DataMetricProp(location)

        name = filename
        if ".txt" in filename:
            name = name[:-4]

        self._plane = PistonEngineMetric1(filename, name, data.get_wingspan(), data.get_chord(),
                                          data.get_swept_angle(), data.get_cruise_altitude(),
                                          data.get_angle_of_attack_at_cruise(), data.get_target_cruise_velocity(),
                                          data.get_max_velocity(), data.get_aircraft_mass(), data.get_cargo_mass(),
                                          data.get_fuel_mass(), data.get_cD0(), data.get_span_efficiency_factor(),
                                          data.get_specific_fuel_consumption(), data.get_propeller_efficiency(),
                                          data.get_engine_power(), data.get_n_structure())

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

    def get_rate_of_climb_at_cruise(self):

        return self._plane.get_rate_of_climb_at_cruise()

    def get_velocity_for_rate_of_climb_at_cruise(self):

        return self._plane.get_velocity_for_rate_of_climb_at_cruise()

    def get_angle_of_climb_at_cruise_in_degrees(self):

        return self._plane.get_angle_of_climb_at_cruise_in_degrees()
