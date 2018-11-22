# Use this file to create the plane objects to find their performances and compare them to each other
# Place the XFLR5 polars into the "AirFoils" folder
# Down below is an example of an aircraft and how to write it to a csv file

import PistonEngine
import TurboJet
import ElectricMotor
import Plane
import XFLR5Data

a = PistonEngine.PistonEngineEnglish2("Design1.txt")
Plane.write_to_csv(a)
a.plot_data()
