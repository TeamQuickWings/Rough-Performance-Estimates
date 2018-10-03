# Kushal Dev Suresh
import math

aT=-(6.5*(10**-3))
TSL=288.16
d=1.225
g0=9.80065
R=287


def get_air_density(h):

    if h == 0:

        return d

    elif 0 < h <= 11000:

        temp = TSL + aT * h
        rho = (temp / TSL)**((-(g0 / (aT * R)))-1) * d
        return rho

    elif 11000 < h <= 25000:

        temp = TSL + aT * 11000
        rho0 = (temp / TSL) ** ((-(g0 / (aT * R)))-1) * d
        rho = math.exp(-(g0 / (R * temp))*(h - 11000)) * rho0
        return rho

    elif h > 25000:

        aS = 3*(10 ** -3)
        temp = (TSL + aT * 11000) + aS*(h-25000)
        temp0 = TSL + aT * 11000
        rho0 = math.exp(-(g0 / (R * temp0)) * (h - 11000)*(temp0 / TSL)**(-(g0/aT)*R)-1)*d
        rho = (temp / temp0) ** ((-(g0 / (aS * R)))-1) * rho0
        return rho
