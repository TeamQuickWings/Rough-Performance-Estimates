# Andrew Scherping
# Abstract class to represent a plane and its estimated performance characteristics
# "ElectricMotor" is class to represent and model the performance of an aircraft with an electric motor
# September 2018
# Last update October 2018
# If there is a '!' please read the comment and make sure the data is filled out properly

import Plane
import AirDensity
import XFLR5Data


class ElectricMotorMetric1(Plane.PlaneMetric):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass,
                 battery_mass, battery_energy, empty_weight_friction, span_efficiency_factor, motor_power,
                 motor_efficiency, propeller_efficiency, n_structure):

        name = "AirFoils/" + filename
        data = XFLR5Data.XFLR5Data(name)

        self._battery_energy = battery_energy
        self._motor_efficiency = motor_efficiency
        self._propeller_efficiency = propeller_efficiency
        self._motor_power = motor_power
        self._air_density = self._air_density = AirDensity.get_air_density_metric(cruise_alt)

        super().__init__(plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt, angle_of_attack_at_cruise,
                         target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass, battery_mass,
                         empty_weight_friction, span_efficiency_factor, n_structure, data.get_alpha_list(),
                         data.get_cl_list(), data.get_cd_list())

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


class ElectricMotorMetric2(Plane.PlaneMetric):

    def __init__(self, filename):

        # Using the "XFLRData" class to extract data from a XFLR5 text file
        location = "AirFoils/" + filename
        data = XFLR5Data.XFLR5DataMetricElectric(location)

        name = filename
        if ".txt" in filename:
            name = name[:-3]

        self._battery_energy = data.get_battery_energy()
        self._motor_efficiency = data.get_motor_efficiency()
        self._propeller_efficiency = data.get_propeller_efficiency()
        self._motor_power = data.get_motor_power()
        self._air_density = self._air_density = AirDensity.get_air_density_metric(data.get_cruise_altitude())

        super().__init__(name, data.get_wingspan(), data.get_chord(), data.get_swept_angle(),
                         data.get_cruise_altitude(), data.get_angle_of_attack_at_cruise(),
                         data.get_target_cruise_velocity(), data.get_max_velocity(), data.get_aircraft_mass(),
                         data.get_cargo_mass(), data.get_fuel_mass(), data.get_empty_weight_friction(),
                         data.get_span_efficiency_factor(), data.get_n_structure(), data.get_alpha_list(),
                         data.get_cl_list(), data.get_cd_list())

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
