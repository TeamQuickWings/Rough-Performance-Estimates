# Use this file to create the plane objects to find their performances and compare them to each other
# Place the XFLR5 polars into the "AirFoils" folder
# All units being used in this program are the SI units (m, s, m/s, kg, N, watts, joules)
# Down below is an example of an aircraft

import PistonEngine
import TurboJet
import ElectricMotor
import Plane

a = PistonEngine.PistonEngine1("NACA_2412_Re5.256.txt", "Cessna 172", 36.09, 4.521, 0, 3000, 2, 122, 163, 1691, 381,
                               377, 0.0175, 0.7, 0.777, .9, 160, 6)
print(a.get_max_range_nm())

b = PistonEngine.PistonEngine2("Cessna172.txt")
print(b.get_max_range_nm())

lst = Plane.PlaneList()
lst.add_plane(a)
lst.add_plane(b)

print(lst.greatest_range().get_name())

