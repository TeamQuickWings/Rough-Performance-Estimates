# Andrew Scherping
# Abstract class to represent a plane and its estimated performance characteristics
# "TurboJet" is class to represent and model the performance of an aircraft with a turbojet or a turbofan
# September 2018
# If there is a '!' please read the comment and make sure the data is filled out properly

import Plane
import math


class TurboJet(Plane.Plane):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, air_density_at_cruise,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass, fuel_mass,
                 empty_weight_friction, span_efficiency_factor, thrust_specific_fuel_consumption,
                 engine_thrust, n_structure):

        self._thrust_specific_fuel_consumption = thrust_specific_fuel_consumption
        self._aircraft_mass = aircraft_mass
        self._cargo_mass = cargo_mass
        self._fuel_mass = fuel_mass
        self._air_density = air_density_at_cruise
        self._engine_thrust = engine_thrust
        self._gravity = 9.81

        super().__init__(filename, plane_airfoil_str, wing_span, chord, swept_angle, air_density_at_cruise,
                         angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass,
                         fuel_mass, empty_weight_friction, span_efficiency_factor, n_structure)

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
