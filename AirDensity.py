# Kushal Dev Suresh
# .py with a method to calculate the air density at a given altitude in meters
# October 2018

# import statements
import math

_c = 0.00194032  # conversation factor from kg/m**3 to slugs/ft**3


# method that returns the air density at given altitude "h"
def get_air_density_english(h):

    # block of constants
    aT = -(6.5 * (10 ** -3))
    TSL = 288.16
    d = 1.225
    g0 = 9.80065
    R = 287
    h = h * 0.3048

    # returns the air density from sea level to 11km
    if 0 <= h <= 11000:

        temp = TSL + aT * h
        rho = (temp / TSL)**((-(g0 / (aT * R)))-1) * d
        return rho * _c

    # returns the air density from 11km to 25 km
    elif 11000 < h <= 25000:

        temp = TSL + aT * 11000
        rho0 = (temp / TSL) ** ((-(g0 / (aT * R))) - 1) * d
        rho = math.exp(-(g0 / (R * temp)) * (h - 11000)) * rho0
        return rho * _c

    # returns the air density above 25km
    elif h > 25000:

        aS = 3 * (10 ** -3)
        temp0 = TSL + aT * 11000
        temp = temp0 + aS * (h - 25000)
        rho0 = math.exp(-(g0 / (R * temp0)) * 14000) * (temp0 / TSL) ** ((-(g0 / (aT * R))) - 1) * d
        print(rho0)
        rho = (temp / temp0) ** ((-(g0 / (aS * R))) - 1) * rho0
        return rho * _c

    # returns -1 if the given altitude is negative
    return -1


# method that returns the air density at given altitude "h"
def get_air_density_metric(h):

    # block of constants
    aT = -(6.5 * (10 ** -3))
    TSL = 288.16
    d = 1.225
    g0 = 9.80065
    R = 287

    # returns the air density from sea level to 11km
    if 0 <= h <= 11000:

        temp = TSL + aT * h
        rho = (temp / TSL)**((-(g0 / (aT * R)))-1) * d
        return rho

    # returns the air density from 11km to 25 km
    elif 11000 < h <= 25000:

        temp = TSL + aT * 11000
        rho0 = (temp / TSL) ** ((-(g0 / (aT * R))) - 1) * d
        rho = math.exp(-(g0 / (R * temp)) * (h - 11000)) * rho0
        return rho

    # returns the air density above 25km
    elif h > 25000:

        aS = 3 * (10 ** -3)
        temp0 = TSL + aT * 11000
        temp = temp0 + aS * (h - 25000)
        rho0 = math.exp(-(g0 / (R * temp0)) * 14000) * (temp0 / TSL) ** ((-(g0 / (aT * R))) - 1) * d
        print(rho0)
        rho = (temp / temp0) ** ((-(g0 / (aS * R))) - 1) * rho0
        return rho

    # returns -1 if the given altitude is negative
    return -1
