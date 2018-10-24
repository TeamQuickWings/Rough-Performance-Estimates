# Use this file to create the plane objects to find their performances and compare them to each other
# Place the XFLR5 polars into the "AirFoils" folder
# All units being used in this program are the SI units (m, s, m/s, kg, N, watts, joules)
# Down below is an example of an aircraft

import PistonEngine
import TurboJet
import ElectricMotor
import Plane
import XFLR5Data

a = PistonEngine.PistonEngineMetric2("Cessna172Metric.txt")
b = PistonEngine.PistonEngineEnglish2("Cessna172.txt")
print(b.get_v_stall_at_cruise())


# b = PistonEngine.PistonEngineEnglish2("Cessna172.txt")
# c = PistonEngine.PistonEngineEnglish1("Cessna172.txt", "Test", 36.09, 4.521, 0, 5000, 0, 122, 163, 1691, 381, 419,
#                                      0.0175, 0.7, 0.777, 0.9, 160, 6)




