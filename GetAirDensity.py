import AirDensity

units = input("Input Unit System (1 - English (ft), 2 - Metric (m)): ")
alt = input("Input the altitude: ")
units = int(units)
alt = float(alt)

if units == 1:

    print(str(AirDensity.get_air_density_english(alt)) + " slugs/ft^3")

elif units == 2:

    print(str(AirDensity.get_air_density_metric(alt)) + " kg/m^3")
