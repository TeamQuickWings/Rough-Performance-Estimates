# Use this file to create the plane objects to find their performances and compare them to each other
# Place the XFLR5 polars into the "AirFoils" folder
# Down below is an example of an aircraft and how to write it to a csv file

import PistonEngine
import TurboJet
import ElectricMotor
import Plane
import XFLR5Data

a = PistonEngine.PistonEngineEnglish2("Design1.txt")
b = PistonEngine.PistonEngineEnglish2("Design2.txt")
c = PistonEngine.PistonEngineEnglish2("Design3.txt")
d = PistonEngine.PistonEngineEnglish2("Design4.txt")
e = PistonEngine.PistonEngineEnglish2("Design5.txt")
Plane.write_to_csv(a)
Plane.write_to_csv(b)
Plane.write_to_csv(c)
Plane.write_to_csv(d)
Plane.write_to_csv(e)

