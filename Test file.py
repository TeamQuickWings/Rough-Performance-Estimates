import PistonEngine
import Plane

a = PistonEngine.PistonEngineMetric2("Cessna172Metric.txt")
b = PistonEngine.PistonEngineEnglish2("Cessna172.txt")
print(a.get_max_endurance())
print(b.get_max_endurance())
