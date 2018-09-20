# Andrew Scherping
# Abstract class to represent a plane and its estimated performance characteristics
# "ElectricMotor" is class to represent and model the performance of an aircraft with an electric motor
# September 2018
# If there is a '!' please read the comment and make sure the data is filled out properly

import Plane
import math


class ElectricMotor(Plane.Plane):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, air_density_at_cruise,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass,
                 battery_mass, battery_energy, empty_weight_friction, span_efficiency_factor, motor_power,
                 motor_efficiency, propeller_efficiency, n_structure):

        self._battery_energy = battery_energy
        self._motor_efficiency = motor_efficiency
        self._propeller_efficiency = propeller_efficiency
        self._motor_power = motor_power
        self._air_density = air_density_at_cruise

        super().__init__(filename, plane_airfoil_str, wing_span, chord, swept_angle, air_density_at_cruise,
                         angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass,
                         battery_mass, empty_weight_friction, span_efficiency_factor, n_structure)

    def get_empty_weight(self):

        return self.get_gross_takeoff_weight()

    def type_of_power_plant(self):

        return "Electric Motor"

    def get_max_range(self):

        clcd_max = (1 / (4 * self.get_K() * self.get_cD0()))
        energy_available = self._battery_energy * self._motor_efficiency * self._propeller_efficiency

        return (energy_available /
                self.get_gross_takeoff_weight()) * clcd_max

    def get_velocity_for_max_range(self):

        return ((2 / self._air_density) * self.get_wing_loading() * ((self.get_K() / self.get_cD0()) ** .5)) ** 0.5

    def get_max_endurance(self):

        cl32cd_max = 0.25 * ((3 / (self.get_K() * (self.get_cD0() ** (1/3)))) ** 0.75)
        energy_available = self._battery_energy * self._motor_efficiency * self._propeller_efficiency

        return ((energy_available * ((self._air_density * self.get_wing_area()) ** 0.25)) /
                ((2 ** .5) * (self.get_gross_takeoff_weight() ** 1.5))) * cl32cd_max

    def get_velocity_for_max_endurance(self):

        return (((2 / self._air_density) * self.get_wing_loading() *
                 ((self.get_K() / (3 * self.get_cD0())) ** 0.5)) ** 0.5)

    def get_max_rate_of_climb(self):

        return -1

    def get_velocity_for_max_rate_of_climb(self):

        return -1

    def get_angle_of_max_rate_of_climb_in_degrees(self):

        return -1
