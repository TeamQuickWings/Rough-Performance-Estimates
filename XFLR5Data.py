import matplotlib.pyplot as plt


class XFLR5DataEnglishJet:

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
                                aircraft_weight=False, cargo_weight=False, fuel_weight=False,
                                empty_weight_friction=False, span_efficiency_factor=False,
                                thrust_specific_fuel_consumption=False, propeller_efficiency=False,
                                engine_thrust=False, n_structure=False)

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

    def get_aircraft_weight(self):

        return self._dictionary.get("aircraft_weight")

    def get_cargo_weight(self):

        return self._dictionary.get("cargo_weight")

    def get_fuel_weight(self):

        return self._dictionary.get("fuel_mass")

    def get_empty_weight_friction(self):

        return self._dictionary.get("empty_weight_friction")

    def get_span_efficiency_factor(self):

        return self._dictionary.get("span_efficiency_factor")

    def get_thrust_specific_fuel_consumption(self):

        return self._dictionary.get("thrust_specific_fuel_consumption")

    def get_engine_thrust(self):

        return self._dictionary.get("engine_thrust")

    def get_n_structure(self):

        return self._dictionary.get("n_structure")


class XFLR5DataMetricJet:

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
                                aircraft_mass=False, cargo_mass=False, fuel_mass=False,
                                empty_weight_friction=False, span_efficiency_factor=False,
                                thrust_specific_fuel_consumption=False, propeller_efficiency=False,
                                engine_thrust=False, n_structure=False)

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

    def get_empty_weight_friction(self):

        return self._dictionary.get("empty_weight_friction")

    def get_span_efficiency_factor(self):

        return self._dictionary.get("span_efficiency_factor")

    def get_thrust_specific_fuel_consumption(self):

        return self._dictionary.get("thrust_specific_fuel_consumption")

    def get_engine_thrust(self):

        return self._dictionary.get("engine_thrust")

    def get_n_structure(self):

        return self._dictionary.get("n_structure")


class XFLR5DataEnglishProp:

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
                                aircraft_weight=False, cargo_weight=False, fuel_weight=False,
                                empty_weight_friction=False, span_efficiency_factor=False,
                                specific_fuel_consumption=False, propeller_efficiency=False, engine_power=False,
                                n_structure=False)

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

    def get_aircraft_weight(self):

        return self._dictionary.get("aircraft_weight")

    def get_cargo_weight(self):

        return self._dictionary.get("cargo_weight")

    def get_fuel_weight(self):

        return self._dictionary.get("fuel_weight")

    def get_empty_weight_friction(self):

        return self._dictionary.get("empty_weight_friction")

    def get_span_efficiency_factor(self):

        return self._dictionary.get("span_efficiency_factor")

    def get_specific_fuel_consumption(self):

        return self._dictionary.get("specific_fuel_consumption")

    def get_propeller_efficiency(self):

        return self._dictionary.get("propeller_efficiency")

    def get_engine_power(self):

        return self._dictionary.get("engine_power")

    def get_n_structure(self):

        return self._dictionary.get("n_structure")


class XFLR5DataMetricProp:

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
                                aircraft_mass=False, cargo_mass=False, fuel_mass=False,
                                empty_weight_friction=False, span_efficiency_factor=False,
                                specific_fuel_consumption=False, propeller_efficiency=False, engine_power=False,
                                n_structure=False)

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

    def get_empty_weight_friction(self):

        return self._dictionary.get("empty_weight_friction")

    def get_span_efficiency_factor(self):

        return self._dictionary.get("span_efficiency_factor")

    def get_specific_fuel_consumption(self):

        return self._dictionary.get("specific_fuel_consumption")

    def get_propeller_efficiency(self):

        return self._dictionary.get("propeller_efficiency")

    def get_engine_power(self):

        return self._dictionary.get("engine_power")

    def get_n_structure(self):

        return self._dictionary.get("n_structure")


class XFLR5DataMetricElectric:

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


class XFLR5Data:

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