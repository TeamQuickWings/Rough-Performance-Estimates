# AIAA Design Compitition
# AIRPLANE AERODYNAMIC PITCHING MOMENT
# realistic Fake values

import matplotlib.pyplot as plt
import numpy as np
import pylab

X_ac_wf = .3  # position of aerodynamic center of wing-fuselage estimated by Part VI of roskams book series
X_ac_h = .85  # position of aerodynamic center of horizontal stabilizer pe
X_cg = .35  # position of the center of mass as a fraction of length X_cg/c
C_L_alpha = -.1
C_m_ac_wf = .1  # moment of the airfoil
C_L_0_wf = .1  # zero lift of the airfoil
C_L_alpha_h = 0
roe = 1.225  # density kg/m^3
velocity_w = 95.1722  # m/s  velocity of aircraft
velocity_t = .9*velocity_w  # velocity at tail
epsilon_0 = 0  # maybe negligible
tau_e = .9  # %Angle of attack effectiveness factor
S_h = 3.4544*1  # reference area of the stabilizer
S = 16.2  # reference of the aircraft wing
q_t = .5*roe*velocity_t**2 # dynamic pressure ratio
q_w = .5*roe*velocity_w**2 # dynamic pressure
nu_h = q_t/q_w  # dynamic pressure ratio
Se = 0.1  # angle rad of stabilizers
V_h = (S_h/S)*(X_ac_h-X_cg)  # look at Part II roskam series for preliminary tail sizing
downwash = .5  # approximate value
i_h = .3
angle_attack =np.linspace(-10, 10, 20)  # angles of attack

C_m_0 = C_m_ac_wf + C_L_0_wf*(X_cg- X_ac_wf)+C_L_alpha_h*nu_h*(S_h/S)*(X_ac_h-X_cg)*epsilon_0
C_m_alpha = C_L_alpha*(X_cg - X_ac_wf) - C_L_alpha_h*nu_h*(S_h/S)*(X_ac_h-X_cg)*(1-downwash)
C_m_i_h = - C_L_alpha_h*nu_h*V_h
C_m_Se = - C_L_alpha_h*nu_h*V_h*tau_e
C_m = C_m_0 + C_m_alpha * angle_attack + C_m_i_h*i_h + C_m_Se * Se  # given equation

plt.plot(angle_attack, C_m)
plt.ylabel('Pitching Moment')
plt.title('Graph')
plt.xlabel('angle of attack')
# plt.show()

# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
Polynomial = np.polynomial.Polynomial

# The data: conc = [P] and absorbance, A
#conc = np.array([0, 20, 40, 80, 120, 180, 260, 400, 800, 1500])
#A = np.array([2.287, 3.528, 4.336, 6.909, 8.274, 12.855, 16.085, 24.797,
#              49.058, 89.400])
gross_Take_off_weight = np.array([2750, 3600, 3400, 3850, 1675, 1670, 2400, 3100, 3350, 3800,
                                 4000, 7750, 2325, 2750, 3600, 2000, 1750, 5100, 1852, 2690,
                                 2138, 1587, 2740, 2900])
empty_weight = np.array([1694, 2195, 2106, 2338, 1100, 1112, 1427, 1757, 1700, 2123, 2426,
                        3385, 1348, 1637, 1935, 1110, 930,  2850, 1125, 1594, 1609, 1256, 1640, 1800])

cmin, cmax = min(gross_Take_off_weight), max(gross_Take_off_weight)
pfit, stats = Polynomial.fit(gross_Take_off_weight, empty_weight, 1, full=True, window=(cmin, cmax),
                                                    domain=(cmin, cmax))

print('Raw fit results:', pfit, stats, sep='\n')

A0, m = pfit
resid, rank, sing_val, rcond = stats
rms = np.sqrt(resid[0]/len(empty_weight))

print('Fit: A = {:.3f}[P] + {:.3f}'.format(m, A0),
      '(rms residual = {:.4f})'.format(rms))

pylab.plot(gross_Take_off_weight, empty_weight, 'o', color='b')
pylab.plot(gross_Take_off_weight, pfit(gross_Take_off_weight), color='k')
pylab.xlabel('Gross takeoff weight')
pylab.ylabel('empty weight')
pylab.show()
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

