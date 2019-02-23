import math

# speed in knots, density in slug/ft^3, lengths in ft, mu in (lbf*s)/ft^2, angles in degrees
cruise_speed = 200
rho = 0.00204834
speed_of_sound = 650.01
mu = 3.68041 * (10 ** -7)
wing_span = 33
chord = 3.6

s_cruise = cruise_speed * 1.687811
s_sound = speed_of_sound * 1.687811
m = s_cruise / s_sound
s_wing = wing_span * chord

# Fuselage
length = 29
width = 5.5
height = 5

r = (rho * length * s_cruise) / mu
cf = 0.455 / ((math.log10(r) ** 2.58) * ((1 + (0.144 * (m ** 2))) ** 0.65))
a_top = 0.5 * length * width
a_side = (4 / 5) * length * height
s_wet = 3.4 * ((a_top + a_side) / 2)
avg = (width + height) / 2
a_max = math.pi * (avg ** 2)
f = length / (((4 / math.pi) * a_max) ** 0.5)
ff = (1 + (60 / (f ** 3)) + (f / 400))
q = 1

cd_fuselage = (cf * ff * q * s_wet) / s_wing

#  Elevator
chord = 2.5
span = 3
swept_angle = 5

r = (rho * chord * s_cruise) / mu
cf = 0.455 / ((math.log10(r) ** 2.58) * ((1 + (0.144 * (m ** 2))) ** 0.65))
t = 0.05 * chord
s_wet = 2.003 * t * span
ff = (1 + ((0.6 / 0.3) * (t / chord)) + (100 * ((t / chord) ** 4))) * \
     ((1.34 * (m ** 0.18)) * (math.cos(swept_angle * (math.pi / 180)) ** 0.28))
q = 1.05

cd_elevator = 2 * ((cf * ff * q * s_wet) / s_wing)

# Vertical Stabilizer
chord = 2.5
height = 3.5
swept_angle = 8

r = (rho * chord * s_cruise) / mu
cf = 0.455 / ((math.log10(r) ** 2.58) * ((1 + (0.144 * (m ** 2))) ** 0.65))
t = 0.05 * chord
s_wet = 2.003 * t * height
ff = (1 + ((0.6 / 0.3) * (t / chord)) + (100 * ((t / chord) ** 4))) * \
     ((1.34 * (m ** 0.18)) * (math.cos(swept_angle * (math.pi / 180)) ** 0.28))
q = 1.05

cd_stabilizer = (cf * ff * q * s_wet) / s_wing

# Engine Nacelle
chord = 5
width = 4
height = 2.5

r = (rho * chord * s_cruise) / mu
cf = 0.455 / ((math.log10(r) ** 2.58) * ((1 + (0.144 * (m ** 2))) ** 0.65))
a_top = (5 / 6) * chord * width
a_side = (4 / 5) * chord * height
s_wet = 3.4 * ((a_top + a_side) / 2)
a_max = (5 / 6) * width * height
f = chord / (((4 / math.pi) * a_max) ** 0.5)
ff = 1 + (0.35 / f)
q = 1.5

cd_engine_nacelles = 2 * ((cf * ff * q * s_wet) / s_wing)

cd = cd_fuselage + cd_elevator + cd_stabilizer + cd_engine_nacelles


def get_drag_coefficient():

    return cd
