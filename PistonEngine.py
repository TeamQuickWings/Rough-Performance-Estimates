# Andrew Scherping
# Abstract class to represent a plane and its estimated performance characteristics
# "PistionEngine" is class to represent and model the performance of an aircraft with a reciprocating piston engine
# or a turboprop
# September 2018
# If there is a '!' please read the comment and make sure the data is filled out properly

import Plane
import math


class PistonEngine(Plane.Plane):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, air_density_at_cruise,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass, fuel_mass,
                 empty_weight_friction, span_efficiency_factor, specific_fuel_consumption, propeller_efficiency,
                 engine_power, n_structure):

        self._specific_fuel_consumption = specific_fuel_consumption
        self._propeller_efficiency = propeller_efficiency
        self._aircraft_mass = aircraft_mass
        self._cargo_mass = cargo_mass
        self._fuel_mass = fuel_mass
        self._air_density = air_density_at_cruise
        self._engine_power = engine_power
        self._gravity = 9.81

        super().__init__(filename, plane_airfoil_str, wing_span, chord, swept_angle, air_density_at_cruise,
                         angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass,
                         fuel_mass, empty_weight_friction, span_efficiency_factor, n_structure)

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
               (0.25 * ((3 / (self.get_K() * (self.get_cD0() ** (1/3)))) ** (3 / 4))) * \
               ((2 * self._air_density * self._wing_area) ** 0.5) * \
               ((1 / (self.get_empty_weight() ** 0.5)) - (1 / (self.get_gross_takeoff_weight() ** 0.5)))

    def get_velocity_for_max_endurance(self):

        return (((2 / self._air_density) * self.get_wing_loading() *
                 ((self.get_K() / (3 * self.get_cD0())) ** 0.5)) ** 0.5)

    def get_max_rate_of_climb(self):

        return ((self._propeller_efficiency * self._engine_power) / self.get_gross_takeoff_weight()) - \
                ((((2 / self._air_density) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())
                  ** 0.5) * (1.155 / ((1 / (4 * self.get_K() * self.get_cD0())) ** 0.5)))

    def get_velocity_for_max_rate_of_climb(self):

        v_climb = ((2 / self._air_density) * ((self.get_K() / (3 * self.get_cD0())) ** 0.5) * self.get_wing_loading())\
                  ** 0.5

        if v_climb < self.get_v_stall():

            return self.get_v_stall()

        else:

            return v_climb

    def get_angle_of_max_rate_of_climb_in_degrees(self):

        return math.degrees(math.atan(self.get_max_rate_of_climb() / self.get_velocity_for_max_rate_of_climb()))
