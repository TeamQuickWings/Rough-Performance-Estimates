# Andrew Scherping
# Abstract class to represent a plane and its estimated performance characteristics
# "Plane" is an abstract class which is a parent to specific types of planes
# September 2018
# Last update October 2018
# If there is a '!' please read the comment and make sure the data is filled out properly

# imports
from abc import abstractmethod
import matplotlib.pyplot as plt
import math
import AirDensity

# gravity constant
_gravity = 32.174


# "Plane class"
class Plane1(object):

    # !
    # "Plane" constructor.
    # Please use English units (ft, s, lb, knots) for all inputted condition, if the condition is an angle use degrees
    # The file input must be a text file, for "plane_airfoil_str" use an identifiable name
    def __init__(self, filename, plane_airfoil_str, wing_span, chord, swept_angle, cruise_alt,
                 angle_of_attack_at_cruise, target_cruise_velocity, max_velocity, aircraft_weight, cargo_weight,
                 fuel_weight, cD0, span_efficiency_factor, n_structure):

        # Using the "XFLRData" class to extract data from a XFLR5 text file
        name = "AirFoils/" + filename
        data = _XFLR5Data(name)

        # Setting variable from the constructor
        self._name = plane_airfoil_str
        self._wing_span = wing_span
        self._alpha = data.get_alpha_list()
        self._clx = data.get_cl_list()
        self._cdx = data.get_cd_list()
        self._target_cruise_velocity = target_cruise_velocity * 1.687811  # converting knots to ft/s
        self._cD0 = cD0
        self._air_density = AirDensity.get_air_density(cruise_alt)
        self._n_structure = n_structure

        # Block to calculate constants used in flight performance
        self._wing_area = wing_span * chord
        aspect_ratio = (wing_span ** 2) / self._wing_area
        self._wing_loading = (aircraft_weight + cargo_weight + fuel_weight) / self._wing_area
        self._k = 1 / (math.pi * span_efficiency_factor * aspect_ratio)
        self._e0 = 0

        if swept_angle == 0:

            self._e0 = (1.78 * (1 - (0.045 * (aspect_ratio ** 0.68)))) - 0.64

        else:

            self._e0 = (4.61 * (1 - (aspect_ratio ** 0.68)) * (math.cos(math.radians(swept_angle)) ** 0.15)) - 3.1

        self._K = 1 / (math.pi * self._e0 * aspect_ratio)

        # set of code to find a linear curve fit of the data in the usable range
        i = 0
        x_sum = 0
        y_sum = 0
        while i < len(self._alpha):

            x_sum += self._alpha[i]
            y_sum += self._clx[i]
            i += 1

        n = len(self._alpha)
        x = x_sum / n
        y = y_sum / n

        i = 0
        x1y1 = 0
        x2 = 0
        while i < len(self._alpha):

            x1y1 += (self._alpha[i] - x) * (self._clx[i] - y)
            x2 += (self._alpha[i] - x) ** 2
            i += 1

        # finding parameters "a0" and "zero_lift_angle"
        self._a0_per_degree = x1y1 / x2
        self._a0_per_radian = self._a0_per_degree * 57.3
        self._b = y - (self._a0_per_degree * x)
        self._zero_lift_angle = -(self._b / self._a0_per_degree)

        # creating a line from "a0_degrees" and "b"
        self._cl = []
        self._alpha_range = []
        for i in range(0, len(self._alpha)):

            self._cl.append((self._a0_per_degree * self._alpha[i]) + self._b)
            self._alpha_range.append(self._alpha[i])

        # Calculating a common constant used in the denominator
        denominator = 1 + (self._a0_per_radian * math.cos(math.radians(swept_angle)) * self._K)

        self._a_per_radian = (self._a0_per_radian * math.cos(math.radians(swept_angle))) / denominator
        self._a_per_degree = self._a_per_radian / 57.3

        # For loop to find the "_cd_at_cruise"
        for i in range(0, len(self._alpha)):

            if self._alpha[i] == angle_of_attack_at_cruise:

                self._cd_at_cruise = self._cdx[i]
                break

        # Block to estimate the 3D CL data at alpha
        # List for 3D CL data
        self._cL = []
        # For loop to add the 3D wing analysis to "cL"
        self._cL_max = 0
        for i in range(0, len(self._alpha)):

            # Equation to estimate cL at angle alpha

            cL_value = (self._a_per_degree * (self._alpha[i] - self._zero_lift_angle))

            self._cL.append(cL_value)

            if self._alpha[i] == angle_of_attack_at_cruise:

                self._cL_at_cruise = cL_value

            if cL_value > self._cL_max:

                self._cL_max = cL_value

        self._cL_slope = (self._cL[len(self._cL) - 1] - self._cL[0]) / len(self._alpha)

        self._cd0 = self._cdx[0]
        for i in range(0, len(self._alpha)):

            temp = self._cdx[i]
            if temp < self._cd0:

                self._cd0 = temp

        # Block to estimate the 3D CD data at alpha
        # List for 3D CD data
        self._cD = []
        self._cd = []
        for i in range(0, len(self._alpha)):

            # Equation to estimate cD at angle alpha
            cD_value = (((self._a_per_degree * (self._alpha[i] - self._zero_lift_angle)) ** 2) * self._K) + \
                       (self._cD0 + self._cd0)
            # Adding "cD_value" to the list "cD"
            self._cD.append(cD_value)
            self._cd.append(self._cd0)

            # If statement to add "cD_value" to "cD0" when alpha is the angle of attack at cruise
            if self._alpha[i] == angle_of_attack_at_cruise:

                self._cD_at_cruise = cD_value

        # Equation for the gross takeoff weight
        self._gross_takeoff_weight = cargo_weight + fuel_weight + aircraft_weight
        # Equation for the empty weight, aircraft weight with no fuel
        self._empty_weight = cargo_weight + aircraft_weight

        # Block to get the thrust and power required at specified velocities
        # Lists for power, trust, and velocity
        self._power = []
        self._thrust = []
        self._velocity = []
        self._min_power_required = 0
        self._min_thrust_required = 0
        self._power_req_at_target_cruise = 0
        self._thrust_req_at_target_cruise = 0
        # Precision of the velocity to calculate power and thrust
        precision = 1
        i = precision
        # While to calculate power and thrust required from 0 m/s to "max_velocity"
        while i <= max_velocity:

            # adding "i" to "velocity"
            self._velocity.append(i / 1.687811)

            # Calculating thrust required
            thrust_required = (.5 * self._air_density * (i ** 2) * self._wing_area * self._cD0) + \
                              ((2 * self._K * self.get_gross_takeoff_weight()) /
                               (self._air_density * (i ** 2) * self._wing_loading))

            # Calculating power required
            power_required = ((.5 * self._air_density * (i ** 3) * self._wing_area * self._cD0) +
                              ((2 * self._K * (self.get_gross_takeoff_weight() ** 2)) /
                              (self._air_density * i * self._wing_area))) / 550  # 550 is the hp conversion

            if self._min_power_required == 0 and self._min_thrust_required == 0:

                self._min_power_required = power_required
                self._min_thrust_required = thrust_required

            else:

                if self._min_power_required > power_required:

                    self._min_power_required = power_required

                if self._min_thrust_required > thrust_required:

                    self._min_thrust_required = thrust_required

            if i == target_cruise_velocity:

                self._power_req_at_target_cruise = power_required
                self._thrust_req_at_target_cruise = thrust_required

            # Adding the calculated values to their list respectively
            self._power.append(power_required)
            self._thrust.append(thrust_required)

            i += precision

    # Abstract method to get the type of power plant
    @abstractmethod
    def type_of_power_plant(self):

        pass

    # Abstract method to get the maximum range in m
    @abstractmethod
    def get_max_range(self):

        pass

    # Abstract method to get the velocity in m/s for the maximum range
    @abstractmethod
    def get_velocity_for_max_range(self):

        pass

    # Abstract method to get the maximum endurance in s
    @abstractmethod
    def get_max_endurance(self):

        pass

    # Abstract method to get the velocity in m/s for the maximum endurance
    @abstractmethod
    def get_velocity_for_max_endurance(self):

        pass

    # Abstract method to get them maximum rate of climb in m/s
    @abstractmethod
    def get_max_rate_of_climb(self):

        pass

    # Abstract method to get the velocity in m/s for the maximum rate of climb
    @abstractmethod
    def get_velocity_for_max_rate_of_climb(self):

        pass

    # Abstract method to get the angle in degrees for the angle of the max rate of climb
    @abstractmethod
    def get_angle_of_max_rate_of_climb_in_degrees(self):

        pass

    # Method to get "_wing_span"
    def get_wing_span(self):

        return self._wing_span

    # Method to return the gross take off weight in N
    def get_gross_takeoff_weight(self):

        return self._gross_takeoff_weight

    # Method that returns the empty weight of the aircraft in N
    def get_empty_weight(self):

        return self._empty_weight

    # Method to return the power required at the target cruise velocity in Watts
    def get_power_required_at_target_cruise_velocity(self):

        return self._power_req_at_target_cruise

    # Method to return the power required at the target cruise velocity in N
    def get_thrust_required_at_target_cruise_velocity(self):

        return self._thrust_req_at_target_cruise

    # Method to get the minimum power required in watts
    def get_minimum_power_required(self):

        return self._min_power_required

    # Method to get the minimum thrust required in N
    def get_minimum_thrust_required(self):

        return self._min_thrust_required

    # Method to get the target cruise velocity
    def get_target_cruise_velocity(self):

        return self._target_cruise_velocity

    # Method to get the "k" value
    def get_k(self):

        return self._k

    # Method to get the variable "K"
    def get_K(self):

        return self._K

    # Method to get CL at cruise
    def get_cL_at_cruise(self):

        return self._cL_at_cruise

    # Method to get CD at cruise
    def get_cD_at_cruise(self):

        return self._cd_at_cruise

    # Method to get the wing loading
    def get_wing_loading(self):

        return self._wing_loading

    # Method to get "cD0"
    def get_cD0(self):

        return self._cD0

    # Method to get the wing surface area in m^2
    def get_wing_area(self):

        return self._wing_area

    # Method to get the maximum CL
    def get_cL_max(self):

        return self._cL_max

    # Method to get the stall velocity in m/s
    def get_v_stall(self):

        return (((2 * self._gross_takeoff_weight) / (self._air_density * self._wing_area * self._cL_max)) ** 0.5) / \
               1.687811

    # Method to get the force of lift in N at the target velocity
    def get_lift_force_at_target_velocity(self):

        return .5 * self._air_density * (self._target_cruise_velocity ** 2) * self._wing_area * self.get_cL_at_cruise()

    # Method to get the n factor at the target velocity
    def get_n_at_target_velocity(self):

        return self.get_lift_force_at_target_velocity() / self._gross_takeoff_weight

    # Method to get the turn radius in m at the target velocity
    def get_turn_radius_at_target_velocity(self):

        if self.get_n_at_target_velocity() < 1:

            print("n < 1. n needs to be greater than 1")
            return -1

        return (self._target_cruise_velocity ** 2) / (_gravity * (((self.get_n_at_target_velocity() ** 2) - 1)
                                                                       ** .5))

    # Method to get the turn rate in degrees/s at the target velocity
    def get_turn_rate_at_target_velocity(self):

        if self.get_n_at_target_velocity() < 1:
            print("n < 1. n needs to be greater than 1")
            return -1

        return math.degrees((_gravity * (((self.get_n_at_target_velocity() ** 2) - 1) ** .5)) /
                            self._target_cruise_velocity)

    # Method to get the maneuvering velocity in m/s
    def get_maneuvering_velocity(self):

        speed = ((((2 * self._n_structure) / (self._air_density * self._cL_max)) * self._wing_loading) ** .5) / 1.687811

        if speed < self.get_v_stall():

            return self.get_v_stall()

        return speed

    # Method to get the turn turn turn radius at the maneuvering velocity in m
    def get_turn_radius_at_maneuvering_velocity(self):

        if self.get_n_at_target_velocity() < 1:

            print("n < 1. n needs to be greater than 1")
            return -1

        return (self.get_maneuvering_velocity() ** 2) / (_gravity * (((self._n_structure ** 2) - 1) ** .5))

    # Method to get the turn rate in degrees/s at the maneuvering velocity
    def get_turn_rate_at_maneuvering_velocity(self):

        if self.get_n_at_target_velocity() < 1:
            print("n < 1. n needs to be greater than 1")
            return -1

        return math.degrees((_gravity * (((self._n_structure ** 2) - 1) ** .5)) / self.get_maneuvering_velocity())

    # Method to get the pull up radius in m at the target velocity
    def get_pull_up_radius_at_target_velocity(self):

        return (self._target_cruise_velocity ** 2) / (_gravity * (self.get_n_at_target_velocity() - 1))

    # Method to get the pull up rate in degrees/s at the target velocity
    def get_pull_up_rate_at_target_velocity(self):

        return math.degrees((_gravity * (self.get_n_at_target_velocity() - 1)) / self._target_cruise_velocity)

    # Method to get the minimum pull up radius in m
    def get_min_pull_up_radius(self):

        return (self.get_maneuvering_velocity() ** 2) / (_gravity * (self._n_structure - 1))

    # Method to get the maximum pull up rate in degrees/s
    def get_max_pull_up_rate(self):

        return math.degrees((_gravity * (self._n_structure - 1)) / self.get_maneuvering_velocity())

    # Method to plot the data
    def plot_data(self):

        fig, axs = plt.subplots(2, 2)

        label1 = "(3D) CL = %.5f (alpha - %.5f)" % (self._cL_slope, self._zero_lift_angle)
        label2 = "(2D) y = %.5f x + %.2f" % (self._a0_per_degree, self._b)
        label3 = "XFLR5 Data"
        axs[0, 0].plot(self._alpha_range, self._cL, "r", label=label1)
        axs[0, 0].plot(self._alpha_range, self._cl, "g", label=label2)
        axs[0, 0].plot(self._alpha, self._clx, "b", label=label3)
        axs[0, 0].set_xlabel("alpha (degrees)")
        axs[0, 0].set_ylabel("cl")
        axs[0, 0].set_title("cl vs. alpha for " + self._name)
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        label4 = "(3D) Drag"
        label5 = "Cd line y = %.5f" % (self._cd[0])
        axs[0, 1].plot(self._clx, self._cdx, "b", label=label3)
        axs[0, 1].plot(self._cl, self._cd, "g", label=label5)
        axs[0, 1].plot(self._cL, self._cD, "r", label=label4)
        axs[0, 1].set_xlabel("Cl")
        axs[0, 1].set_ylabel("Cd")
        axs[0, 1].set_title("Cd vs. Cl")
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        label6 = "Thrust (N)"
        label7 = "Power (watts)"
        axs2 = axs[1, 0].twinx()
        axs2.plot(self._velocity, self._thrust, "b", label=label6)
        axs2.set_ylabel("Thrust (N)")
        axs2.legend()
        axs[1, 0].plot(self._velocity, self._power, "r", label=label7)
        axs[1, 0].set_ylim(0, 60000)
        axs[1, 0].set_xlabel("Velocity (m/s")
        axs[1, 0].set_ylabel("Power (watts)")
        axs[1, 0].set_title("Thrust Required and Power Required vs. Velocity")
        axs[1, 0].legend()
        axs[1, 0].grid(True)

        plt.show()

    # Method to get the name of the plane
    def get_name(self):

        return self._name


class Plane2(object):

    def __init__(self, name, wing_span, chord, swept_angle, cruise_alt, angle_of_attack_at_cruise,
                 target_cruise_velocity, max_velocity, aircraft_weight, cargo_weight, fuel_weight, cD0,
                 span_efficiency_factor, n_structure, alpha, cl, cd):

        # Setting variable from the constructor
        self._name = name
        self._wing_span = wing_span
        self._alpha = alpha
        self._clx = cl
        self._cdx = cd
        self._target_cruise_velocity = target_cruise_velocity
        self._cD0 = cD0
        self._air_density = AirDensity.get_air_density(cruise_alt)
        self._n_structure = n_structure

        # Block to calculate constants used in flight performance
        self._wing_area = wing_span * chord
        aspect_ratio = (wing_span ** 2) / self._wing_area
        self._wing_loading = (aircraft_weight + cargo_weight + fuel_weight) / self._wing_area
        self._k = 1 / (math.pi * span_efficiency_factor * aspect_ratio)
        self._e0 = 0

        if swept_angle == 0:

            self._e0 = (1.78 * (1 - (0.045 * (aspect_ratio ** 0.68)))) - 0.64

        else:

            self._e0 = (4.61 * (1 - (aspect_ratio ** 0.68)) * (math.cos(math.radians(swept_angle)) ** 0.15)) - 3.1

        self._K = 1 / (math.pi * self._e0 * aspect_ratio)

        # set of code to find a linear curve fit of the data in the usable range
        i = 0
        x_sum = 0
        y_sum = 0
        while i < len(self._alpha):
            x_sum += self._alpha[i]
            y_sum += self._clx[i]
            i += 1

        n = len(self._alpha)
        x = x_sum / n
        y = y_sum / n

        i = 0
        x1y1 = 0
        x2 = 0
        while i < len(self._alpha):
            x1y1 += (self._alpha[i] - x) * (self._clx[i] - y)
            x2 += (self._alpha[i] - x) ** 2
            i += 1

        # finding parameters "a0" and "zero_lift_angle"
        self._a0_per_degree = x1y1 / x2
        self._a0_per_radian = self._a0_per_degree * 57.3
        self._b = y - (self._a0_per_degree * x)
        self._zero_lift_angle = -(self._b / self._a0_per_degree)

        # creating a line from "a0_degrees" and "b"
        self._cl = []
        self._alpha_range = []
        for i in range(0, len(self._alpha)):
            self._cl.append((self._a0_per_degree * self._alpha[i]) + self._b)
            self._alpha_range.append(self._alpha[i])

        # Calculating a common constant used in the denominator
        denominator = 1 + (self._a0_per_radian * math.cos(math.radians(swept_angle)) * self._K)

        self._a_per_radian = (self._a0_per_radian * math.cos(math.radians(swept_angle))) / denominator
        self._a_per_degree = self._a_per_radian / 57.3

        # For loop to find the "_cd_at_cruise"
        for i in range(0, len(self._alpha)):

            if self._alpha[i] == angle_of_attack_at_cruise:
                self._cd_at_cruise = self._cdx[i]
                break

        # Block to estimate the 3D CL data at alpha
        # List for 3D CL data
        self._cL = []
        # For loop to add the 3D wing analysis to "cL"
        self._cL_max = 0
        for i in range(0, len(self._alpha)):

            # Equation to estimate cL at angle alpha

            cL_value = (self._a_per_degree * (self._alpha[i] - self._zero_lift_angle))

            self._cL.append(cL_value)

            if self._alpha[i] == angle_of_attack_at_cruise:
                self._cL_at_cruise = cL_value

            if cL_value > self._cL_max:
                self._cL_max = cL_value

        self._cL_slope = (self._cL[len(self._cL) - 1] - self._cL[0]) / len(self._alpha)

        self._cd0 = self._cdx[0]
        for i in range(0, len(self._alpha)):

            temp = self._cdx[i]
            if temp < self._cd0:
                self._cd0 = temp

        # Block to estimate the 3D CD data at alpha
        # List for 3D CD data
        self._cD = []
        self._cd = []
        for i in range(0, len(self._alpha)):

            # Equation to estimate cD at angle alpha
            cD_value = (((self._a_per_degree * (self._alpha[i] - self._zero_lift_angle)) ** 2) * self._K) + \
                       (self._cD0 + self._cd0)
            # Adding "cD_value" to the list "cD"
            self._cD.append(cD_value)
            self._cd.append(self._cd0)

            # If statement to add "cD_value" to "cD0" when alpha is the angle of attack at cruise
            if self._alpha[i] == angle_of_attack_at_cruise:
                self._cD_at_cruise = cD_value

        # Equation for the gross takeoff weight
        self._gross_takeoff_weight = cargo_weight + fuel_weight + aircraft_weight
        # Equation for the empty weight, aircraft weight with no fuel
        self._empty_weight = cargo_weight + aircraft_weight

        # Block to get the thrust and power required at specified velocities
        # Lists for power, trust, and velocity
        self._power = []
        self._thrust = []
        self._velocity = []
        self._min_power_required = 0
        self._min_thrust_required = 0
        self._power_req_at_target_cruise = 0
        self._thrust_req_at_target_cruise = 0
        # Precision of the velocity to calculate power and thrust
        precision = 1
        i = precision
        # While to calculate power and thrust required from 0 m/s to "max_velocity"
        while i <= max_velocity:

            # adding "i" to "velocity"
            self._velocity.append(i / 1.687811)

            # Calculating thrust required
            thrust_required = (.5 * self._air_density * (i ** 2) * self._wing_area * self._cD0) + \
                              ((2 * self._K * self.get_gross_takeoff_weight()) /
                               (self._air_density * (i ** 2) * self._wing_loading))

            # Calculating power required
            power_required = ((.5 * self._air_density * (i ** 3) * self._wing_area * self._cD0) +
                              ((2 * self._K * (self.get_gross_takeoff_weight() ** 2)) /
                               (self._air_density * i * self._wing_area))) / 550  # 550 is the hp conversion

            if self._min_power_required == 0 and self._min_thrust_required == 0:

                self._min_power_required = power_required
                self._min_thrust_required = thrust_required

            else:

                if self._min_power_required > power_required:
                    self._min_power_required = power_required

                if self._min_thrust_required > thrust_required:
                    self._min_thrust_required = thrust_required

            if i == target_cruise_velocity:
                self._power_req_at_target_cruise = power_required
                self._thrust_req_at_target_cruise = thrust_required

            # Adding the calculated values to their list respectively
            self._power.append(power_required)
            self._thrust.append(thrust_required)

            i += precision

    # Abstract method to get the type of power plant
    @abstractmethod
    def type_of_power_plant(self):

        pass

    # Abstract method to get the maximum range in m
    @abstractmethod
    def get_max_range_nm(self):

        pass

    # Abstract method to get the velocity in m/s for the maximum range
    @abstractmethod
    def get_velocity_for_max_range_knots(self):

        pass

    # Abstract method to get the maximum endurance in s
    @abstractmethod
    def get_max_endurance_min(self):

        pass

    # Abstract method to get the velocity in m/s for the maximum endurance
    @abstractmethod
    def get_velocity_for_max_endurance_knots(self):

        pass

    # Abstract method to get them maximum rate of climb in m/s
    @abstractmethod
    def get_max_rate_of_climb_ft_per_s(self):

        pass

    # Abstract method to get the velocity in m/s for the maximum rate of climb
    @abstractmethod
    def get_velocity_for_max_rate_of_climb_knots(self):

        pass

    # Abstract method to get the angle in degrees for the angle of the max rate of climb
    @abstractmethod
    def get_angle_of_max_rate_of_climb_in_degrees(self):

        pass

    # Method to get "_wing_span"
    def get_wing_span(self):

        return self._wing_span

    # Method to return the gross take off weight in N
    def get_gross_takeoff_weight(self):

        return self._gross_takeoff_weight

    # Method that returns the empty weight of the aircraft in N
    def get_empty_weight(self):

        return self._empty_weight

    # Method to return the power required at the target cruise velocity in Watts
    def get_power_required_at_target_cruise_velocity(self):

        return self._power_req_at_target_cruise

    # Method to return the power required at the target cruise velocity in N
    def get_thrust_required_at_target_cruise_velocity(self):

        return self._thrust_req_at_target_cruise

    # Method to get the minimum power required in watts
    def get_minimum_power_required(self):

        return self._min_power_required

    # Method to get the minimum thrust required in N
    def get_minimum_thrust_required(self):

        return self._min_thrust_required

    # Method to get the target cruise velocity
    def get_target_cruise_velocity(self):

        return self._target_cruise_velocity

    # Method to get the "k" value
    def get_k(self):

        return self._k

    # Method to get the variable "K"
    def get_K(self):

        return self._K

    # Method to get CL at cruise
    def get_cL_at_cruise(self):

        return self._cL_at_cruise

    # Method to get CD at cruise
    def get_cD_at_cruise(self):

        return self._cd_at_cruise

    # Method to get the wing loading
    def get_wing_loading(self):

        return self._wing_loading

    # Method to get "cD0"
    def get_cD0(self):

        return self._cD0

    # Method to get the wing surface area in m^2
    def get_wing_area(self):

        return self._wing_area

    # Method to get the maximum CL
    def get_cL_max(self):

        return self._cL_max

    # Method to get the stall velocity in m/s
    def get_v_stall(self):

        return (((2 * self._gross_takeoff_weight) / (self._air_density * self._wing_area * self._cL_max)) ** 0.5) / \
               1.687811

    # Method to get the force of lift in N at the target velocity
    def get_lift_force_at_target_velocity(self):

        return .5 * self._air_density * (self._target_cruise_velocity ** 2) * self._wing_area * self.get_cL_at_cruise()

    # Method to get the n factor at the target velocity
    def get_n_at_target_velocity(self):

        return self.get_lift_force_at_target_velocity() / self._gross_takeoff_weight

    # Method to get the turn radius in m at the target velocity
    def get_turn_radius_at_target_velocity(self):

        if self.get_n_at_target_velocity() < 1:
            print("n < 1. n needs to be greater than 1")
            return -1

        return (self._target_cruise_velocity ** 2) / (_gravity * (((self.get_n_at_target_velocity() ** 2) - 1) ** .5))

    # Method to get the turn rate in degrees/s at the target velocity
    def get_turn_rate_at_target_velocity(self):

        if self.get_n_at_target_velocity() < 1:
            print("n < 1. n needs to be greater than 1")
            return -1

        return math.degrees((_gravity * (((self.get_n_at_target_velocity() ** 2) - 1) ** .5)) /
                            self._target_cruise_velocity)

    # Method to get the maneuvering velocity in m/s
    def get_maneuvering_velocity(self):

        speed = ((((2 * self._n_structure) / (self._air_density * self._cL_max)) * self._wing_loading) ** .5) / 1.687811

        if speed < self.get_v_stall():
            return self.get_v_stall()

        return speed

    # Method to get the turn turn turn radius at the maneuvering velocity in m
    def get_turn_radius_at_maneuvering_velocity(self):

        if self.get_n_at_target_velocity() < 1:
            print("n < 1. n needs to be greater than 1")
            return -1

        return (self.get_maneuvering_velocity() ** 2) / (_gravity * (((self._n_structure ** 2) - 1) ** .5))

    # Method to get the turn rate in degrees/s at the maneuvering velocity
    def get_turn_rate_at_maneuvering_velocity(self):

        if self.get_n_at_target_velocity() < 1:
            print("n < 1. n needs to be greater than 1")
            return -1

        return math.degrees((_gravity * (((self._n_structure ** 2) - 1) ** .5)) / self.get_maneuvering_velocity())

    # Method to get the pull up radius in m at the target velocity
    def get_pull_up_radius_at_target_velocity(self):

        return (self._target_cruise_velocity ** 2) / (_gravity * (self.get_n_at_target_velocity() - 1))

    # Method to get the pull up rate in degrees/s at the target velocity
    def get_pull_up_rate_at_target_velocity(self):

        return math.degrees((_gravity * (self.get_n_at_target_velocity() - 1)) / self._target_cruise_velocity)

    # Method to get the minimum pull up radius in m
    def get_min_pull_up_radius(self):

        return (self.get_maneuvering_velocity() ** 2) / (_gravity * (self._n_structure - 1))

    # Method to get the maximum pull up rate in degrees/s
    def get_max_pull_up_rate(self):

        return math.degrees((_gravity * (self._n_structure - 1)) / self.get_maneuvering_velocity())

    # Method to plot the data
    def plot_data(self):

        fig, axs = plt.subplots(2, 2)

        label1 = "(3D) CL = %.5f (alpha - %.5f)" % (self._cL_slope, self._zero_lift_angle)
        label2 = "(2D) y = %.5f x + %.2f" % (self._a0_per_degree, self._b)
        label3 = "XFLR5 Data"
        axs[0, 0].plot(self._alpha_range, self._cL, "r", label=label1)
        axs[0, 0].plot(self._alpha_range, self._cl, "g", label=label2)
        axs[0, 0].plot(self._alpha, self._clx, "b", label=label3)
        axs[0, 0].set_xlabel("alpha (degrees)")
        axs[0, 0].set_ylabel("cl")
        axs[0, 0].set_title("cl vs. alpha for " + self._name)
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        label4 = "(3D) Drag"
        label5 = "Cd line y = %.5f" % (self._cd[0])
        axs[0, 1].plot(self._clx, self._cdx, "b", label=label3)
        axs[0, 1].plot(self._cl, self._cd, "g", label=label5)
        axs[0, 1].plot(self._cL, self._cD, "r", label=label4)
        axs[0, 1].set_xlabel("Cl")
        axs[0, 1].set_ylabel("Cd")
        axs[0, 1].set_title("Cd vs. Cl")
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        label6 = "Thrust (N)"
        label7 = "Power (watts)"
        axs2 = axs[1, 0].twinx()
        axs2.plot(self._velocity, self._thrust, "b", label=label6)
        axs2.set_ylabel("Thrust (N)")
        axs2.legend()
        axs[1, 0].plot(self._velocity, self._power, "r", label=label7)
        axs[1, 0].set_ylim(0, 60000)
        axs[1, 0].set_xlabel("Velocity (m/s")
        axs[1, 0].set_ylabel("Power (watts)")
        axs[1, 0].set_title("Thrust Required and Power Required vs. Velocity")
        axs[1, 0].legend()
        axs[1, 0].grid(True)

        plt.show()

    # Method to get the name of the plane
    def get_name(self):

        return self._name


class PlaneList:

    def __init__(self):

        self.lst = []

    def add_plane(self, plane):

        if len(self.lst) == 0:

            self.lst.append(plane)

        else:

            found = False

            for i in self.lst:

                if plane.get_name() == i.get_name():

                    found = True
                    break

            if not found:

                self.lst.append(plane)

    def remove_plane(self, plane):

        self.lst.remove(plane)

    def get_length(self):

        return len(self.lst)

    def greatest_endurance(self):

        a = self.lst[0]

        for i in self.lst:

            if a.get_max_endurance_min() < i.get_max_endurance_min():

                a = i

        return a

    def greatest_range(self):

        a = self.lst[0]

        for i in self.lst:

            if a.get_max_range_nm() < i.get_max_range_nm():

                a = i

        return a


class _XFLR5Data:

    def __init__(self, filename):

        file = open(filename, "r")
        data = []

        for i in file:

            data.append(i)

        file.close()

        self._alpha = []
        _alpha_index = -1
        self._cl = []
        _cl_index = -1
        self._cd = []
        _cd_index = -1
        self._got_angles = False

        got_column_titles = False
        for i in data:

            data_set = i.split()
            index = 0
            if "angles:" in data_set:

                if len(data_set) == 3:

                    self._start_angle = float(data_set[1])
                    self._end_angle = float(data_set[2])
                    self._got_angles = True

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
            p.set_title("cl vs. alpha for " + filename)
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
