# Andrew Scherping
# Abstract class to represent a plane and its estimated performance characteristics
# "ElectricMotor" is class to represent and model the performance of an aircraft with an electric motor
# September 2018
# If there is a '!' please read the comment and make sure the data is filled out properly

import Plane
import math
import AirDensity
import matplotlib.pyplot as plt


class ElectricMotor1(Plane.Plane1):

    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_mass, cargo_mass,
                 battery_mass, battery_energy, empty_weight_friction, span_efficiency_factor, motor_power,
                 motor_efficiency, propeller_efficiency, n_structure):

        self._battery_energy = battery_energy
        self._motor_efficiency = motor_efficiency
        self._propeller_efficiency = propeller_efficiency
        self._motor_power = motor_power
        self._air_density = self._air_density = AirDensity.get_air_density(cruise_alt)

        super().__init__(filename, plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
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


class ElectricMotor2(Plane.Plane2):

    def __init__(self, filename):

        # Using the "XFLRData" class to extract data from a XFLR5 text file
        location = "AirFoils/" + filename
        data = _XFLR5Data(location)

        name = filename
        if ".txt" in filename:
            name = name[:-3]

        self._battery_energy = battery_energy
        self._motor_efficiency = motor_efficiency
        self._propeller_efficiency = propeller_efficiency
        self._motor_power = motor_power
        self._air_density = self._air_density = AirDensity.get_air_density(cruise_alt)

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

class _XFLR5Data:

    def __init__(self, filename):

        file = open(filename, "r")
        data = []

        name = filename
        if name.endswith(".txt"):
            name = name[:-3]

        for i in file:

            data.append(i)

        file.close()

        self._alpha = []
        _alpha_index = -1
        self._cl = []
        _cl_index = -1
        self._cd = []
        _cd_index = -1
        got_column_titles = False
        self._got_angles = False
        self._dictionary = dict(wingspan=False, chord=False, swept_angle=False, cruise_altitude=False,
                                angle_of_attack_at_cruise=False, target_cruise_velocity=False, max_velocity=False,
                                aircraft_mass=False, cargo_mass=False, fuel_mass=False, battery_energy=False,
                                empty_weight_friction=False, span_efficiency_factor=False, propeller_efficiency=False,
                                motor_efficiency=False, motor_power=False, n_structure=False)

        for i in data:

            data_set = i.split()
            index = 0
            if "angles:" in data_set:

                if len(data_set) == 3:

                    self._start_angle = float(data_set[1])
                    self._end_angle = float(data_set[2])
                    self._got_angles = True

            for j in self._dictionary:

                for k in data_set:

                    if j in k:

                        if len(data_set) == 2:

                            self._dictionary[j] = float(data_set[1])

            if len(data_set) > 0:

                if _is_number(data_set[0]) is False and not got_column_titles:

                    string_split = i.split()

                    for j in string_split:

                        if "alpha" in j:

                            _alpha_index = index

                        if "CL" in j:

                            _cl_index = index

                        if "CD" in j:

                            _cd_index = index

                        index += 1

                        if _alpha_index > -1 and _cl_index > -1 and _cd_index > -1:

                            got_column_titles = True
                            break

                if got_column_titles and _is_number(data_set[0]):

                    self._alpha.append(float(data_set[_alpha_index]))
                    self._cl.append(float(data_set[_cl_index]))
                    self._cd.append(float(data_set[_cd_index]))

        if self._got_angles:

            start_angle = self._start_angle
            end_angle = self._end_angle

        else:

            # Block to plot data from the XFLR5 file to determine an acceptable range for usable data
            # Creates a plot of "_cl" vs. "_alpha"
            fig = plt.figure()
            p = fig.subplots()
            p.plot(self._alpha, self._cl, "b")
            p.set_xlabel("alpha (degrees)")
            p.set_ylabel("cl")
            p.set_title("cl vs. alpha for " + name)
            plt.grid(True)
            plt.show()

            # Asking the using to input the acceptable range for usable data
            start_angle = float(input("Enter starting angle (must be an angle in the file): "))
            end_angle = float(input("Enter last angle  (must be an angle in the file): "))

        # while loop to find the starting index of usable data
        start_index = 0
        while start_angle != self._alpha[start_index]:
            start_index += 1

        # while loop to find the ending index of usable data
        end_index = 0
        while end_angle != self._alpha[end_index]:
            end_index += 1

        self._alpha = self._alpha[start_index:end_index]
        self._cl = self._cl[start_index:end_index]
        self._cd = self._cd[start_index:end_index]

    def get_alpha_list(self):

        return self._alpha

    def get_cl_list(self):

        return self._cl

    def get_cd_list(self):

        return self._cd

    def got_angles(self):

        return self._got_angles

    def get_start_angle(self):

        return self._start_angle

    def get_end_angle(self):

        return self._end_angle

    def get_wingspan(self):

        return self._dictionary.get("wingspan")

    def get_chord(self):

        return self._dictionary.get("chord")

    def get_swept_angle(self):

        return self._dictionary.get("swept_angle")

    def get_cruise_altitude(self):

        return self._dictionary.get("cruise_altitude")

    def get_angle_of_attack_at_cruise(self):

        return self._dictionary.get("angle_of_attack_at_cruise")

    def get_target_cruise_velocity(self):

        return self._dictionary.get("target_cruise_velocity")

    def get_max_velocity(self):

        return self._dictionary.get("max_velocity")

    def get_aircraft_mass(self):

        return self._dictionary.get("aircraft_mass")

    def get_cargo_mass(self):

        return self._dictionary.get("cargo_mass")

    def get_fuel_mass(self):

        return self._dictionary.get("fuel_mass")

    def get_battery_energy(self):

        return self._dictionary.get("battery_energy")

    def get_empty_weight_friction(self):

        return self._dictionary.get("empty_weight_friction")

    def get_span_efficiency_factor(self):

        return self._dictionary.get("span_efficiency_factor")

    def get_propeller_efficiency(self):

        return self._dictionary.get("propeller_efficiency")

    def get_motor_efficiency(self):

        return self._dictionary.get("motor_efficiency")

    def get_motor_power(self):

        return self._dictionary.get("motor_power")

    def get_n_structure(self):

        return self._dictionary.get("n_structure")


# private method to determine in an input is a number
def _is_number(s):

    try:

        float(s)
        return True

    except ValueError:

        pass

    try:

        import unicodedata
        unicodedata.numeric(s)
        return True

    except (TypeError, ValueError):

        pass

    return False
