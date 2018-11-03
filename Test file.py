import PistonEngine
import Plane

b = PistonEngine.PistonEngineEnglish2("Cessna172.txt")
print(b.get_name())
Plane.write_to_csv(b)
