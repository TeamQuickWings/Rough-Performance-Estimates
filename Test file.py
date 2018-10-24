import PistonEngine

dictionary = dict(angles=False, wingspan=False, swept_angle=False, cruise_altitude=False,
                  angle_of_attack_at_cruise=False)

dictionary["swept_angle"] = 0

for i in dictionary:

    if i in "swept_angle":

        dictionary[i] = 10

a = [1, 2, 3, 4, 5]
a = a[1:4]

b = PistonEngine.PistonEngine2("Cessna172.txt")
b.plot_data()
