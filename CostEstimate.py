# Nathan Briggs, Andrew Scherping
# Code to estimate the operating costs of an aircraft
# time is in hours and and distance in nm

number_of_engines = 1 # not used anywhere
take_off_weight = 900
block_distance = 135
cruise_velocity = 180
operation_years = 20
crew_hours = 800
time_to_cruise = 0.42

maneuver_time_from_atc = 0.25 * 10 ** (-6) * take_off_weight + 0.0625
distance_from_atc_maneuvering = cruise_velocity * maneuver_time_from_atc
distance_of_decent = 90
distance_of_climb = 100
time_in_cruise = (1.06 * block_distance - distance_of_climb - distance_of_decent + distance_from_atc_maneuvering) \
                 / cruise_velocity
time_on_ground = 0.51 * 10 ** (-6) * take_off_weight + 0.125
time_block = time_on_ground + time_to_cruise + time_in_cruise + t_de # what is t_de?
annual_use = 1000 * (3.4546 * time_block + 2.944 - 12.289 * time_block ** 2 - 5.6626 * time_block + 8.964) ** 0.5

block_speed = block_distance / time_block
pilot_salary = 85000
cost_of_crew = cost_of_crew + 2 * ((1.26 / block_speed) * (pilot_salary / 800) + 7 / block_speed) # cost_of_crew in its own equation?

fuel_density = 6.7
fuel_price = 5
weight_of_fuel = 200
fuel_and_oil_cost = 1.05 * (weight_of_fuel / block_distance) * fuel_price / fuel_density
flight_operating_costs = cost_of_crew + fuel_and_oil_cost

fee_per_landing = 0.002 * take_off_weight
C_lf = fee_per_landing / (block_speed * time_block) # what?
DOC_lnr = C_lf # what?

DOC = (1 / 0.98) * (1 / 0.93) * (flight_operating_costs + DOC_maint + DOC_lnr) # DOC_maint not mentioned anywhere
