# CG_estimate calculation
# Statistical Weight Estimation Methods
import math
# -------------------------------------------------------------------------------------------------------------
S_w = 154  # Trapezodial wing area
W_fw = 600  # weight of fuel in wing in lbf
W_fw_h = 1  # tail section fuel weight
W_fw_v = 1
AR_wing = 9
lambda_4 = math.radians(0)  # sweep of wing at quater point
t_r = 1  # Taper ratio
t_c = .12   # wing thickness to chord ratio
roe = 23.77*(10**-4)  # density of air (10-4 slugs/ft3)
V = 180*1.1  # velocity
q = .5*roe*V**2
n_z = 6.4  # ultimate load factor
W_o = 4000  # design gross wight in lbf
V_H = 180  # maximum level airsped as S_Lin KEAS
#  predicted Weight of wing in lbf

# Raymer
W_w = .036*(S_w**.758)*(W_fw**.0035)*((AR_wing/(math.cos(lambda_4)**2))**.6)*(q**.006)*(t_r**.04)*(((100*t_c)/(math.cos(lambda_4)**2))**(-.3))*((n_z*W_o)**.49)
print("Raymer W_w =", W_w)

W_w1 = 96.6948*(((((n_z*W_o)/(10**5))**.65)*((AR_wing/(math.cos(lambda_4)**2))**.57)*((S_w/100)**.61)*(((1+t_r)/(2*t_c))**.36)*((1+(V_H/500))**.5))**.993)
print("Nicolai W_w =", W_w1)

# ----------------------------------------------------------------------------------
# Horizontal tail (HT) weight
# predicted weight of tail in lbf
AR_HT = 3 # ????  Aspect ratio
S_HT = 20  # trapezoidal Ht area in ft^2
lambda_HT = math.radians(25)  # HT sweep at 25% MGC
t_r_HT = .5  # HT Taper ratio
l_HT = 15  # horizontal Tail arm from wing C/4 to HT C/4 in ft
b_HT = 6  # HT span in ft
t_HT_max = 3  # max root chord thickness of ht in inches
t_c_HT = .12  # thickness ration for tail

W_HT = .016*((n_z*W_o)**.414)*(q**.168)*(S_HT**.896)*(((100*t_c_HT)/(math.cos(lambda_HT)))**(-.12))*((AR_HT/((math.cos(lambda_HT))**2))**(.043))*(t_r_HT**(-.02))
print("Raymer W_HT = ", W_HT)

W_HT1 = 127*(((((n_z*W_o)/(10**5))**.87)*((S_HT/100)**1.2)*((l_HT/10)**.483)*((b_HT/t_HT_max)**.5))**.458)
print("Nicolai W_HT = ", W_HT1)

# ----------------------------------------------------------------------------------
# Vertical Tail (VT) Weight
# predicted weight of VT in lbf
F_tail = 0  # for conventional tail, =1 for T-tail
S_VT = 12  # Trapezoidal VT area in ft^2
lambda_VT = math.radians(65)  # VT Sweep at 25% MGC
t_r_VT = .3  # taper Ratio for VT
b_VT = 6  # HT span in ft
t_VT_max = 5  # max root chord thickness of VT in inches
t_c_VT = .12 # Thickness ratio of VT
AR_VT = 4

W_VT = .073*(1+.2*F_tail)*((n_z*W_o)**.376)*(q**.122)*(S_VT**.873)*(((100*t_c)/(math.cos(lambda_VT)))**(-.49))*((AR_VT/((math.cos(lambda_VT))**2))**.357)*(t_r_VT**.039)
print("Raymer W_VT = ", W_VT)

W_VT1 = 985*(((n_z*W_o/(10**5))**.87)*((S_VT/100)**1.2)*((b_VT/t_VT_max)**(1/2)))
print("Nicolai W_VT = " + str(W_VT1) + "  WRONG")

#  -----------------------------------------------------------------------
# Fuselage Weight
# Predicted weight of the fuselage in lbf
A_top = 5
A_side = 28
S_FUS = 3.4*((A_top+A_side)/2)  # wetted area in ft^2
l_FS = 30  # length of fuselage structure (forward bulkhead to aft frame in ft
d_FS = 5  # depth of fuselage structure in ft
V_p = 150  # Volume of pressurized cabin section in ft^3
Del_P = 0  # cabin pressure differential in psi
l_F = 30  # Fuselage length in ft
W_F = 5  # Fuselage max width in ft
d_F = 5  # Fuselage max depth in ft

W_FUS = (.052*(S_FUS**1.086)*((n_z*W_o)**.177)*(l_HT**(-.051))*((l_FS/d_FS)**(-.072))*(q**.241)) + (11.9*(V_p*Del_P)**.271)
print("Raymer W_FUS = ", W_FUS) # i believe this is for structure and skill don't think it is very accurate

W_FUS1 = 200*((((n_z*W_o/(10**5))**.286)*((l_F/10)**.857)*((W_F + d_F)/10)*((V_H/100)**.338))**1.1)
print("Nicolai W_FUS", W_FUS1)

# ---------------------------------------------------------------------------------------------------------------------
# Main Landing Gear Weight
n1 = 3  # Ultimate landing load factor
W1 = 4000  # designed landing weight in lbf
L_m = 36  # Length of the main landing gear strut in inches
L_n = 36  # Length of nose landing gear strut in inches

W_MLG = .095 *((n1 *W1)**.768)*((L_m/12)**.409)
print("Raymer Main landing gear W_MLG = ", W_MLG)

W_NLG = .125*((n1*W1)**.566)*((L_n/12)**.845)
print("Raymer Nose landing gear W_NLG = ", W_NLG)

W_MLG1 = .054*((n1 *W1)**.684)*((L_m/12)**.601)
print("Nicolai Entire landing gear W_MNLG = ", W_MLG1)
# --------------------------------------------------------------------------------------------------------------------
# Installed Engine Weight
W_Eng = 1000  # weight of the engine in lbs
N_eng = 1  # number of engines

W_EI = 2.575*W_Eng**.922*N_eng
print("both W_EI = ", W_EI)
# -------------------------------------------------------------------------------------------------------------------
# fuel system Weight
Q_tot = 600  # total fuel quantity in gallons
Q_int = 0 # fuel quantity in integral fuel tanks in gallons
N_Tank = 2 # number of tanks

W_FS = 2.49*(Q_tot**.726)*((Q_tot/(Q_tot+Q_int))**.363)*(N_Tank**.242)*(N_eng**.157)
print("Raymer W_FS = ", W_FS)

W_FS1 = 2.49*(((Q_tot**.6)*((Q_tot/(Q_tot+Q_int))**.3)*(N_Tank**.2)*(N_eng**.13))**1.21)
print("Nicolai W_FS", W_FS1)

# -------------------------------------------------------------------------------------------------------------------
# Flight COntrol System Weight
b = 33# wingspan in ft
W_CTRL = .053*(l_FS**1.536)*(b**.371)*((n_z*W_o*10**(-4))**.8)
print("Raymer W_CTRL = ", W_CTRL)

W_pow_CTRL = 1.08*(W_o**.7)
W_man_CTRL = 1.066*(W_o**.626)
print("Nicolai W_pow_CTRL = ", W_pow_CTRL)
print("Nicolai W_man_CTRL = ", W_man_CTRL)
# -----------------------------------------------------------------------------------------------------------------
# hydraulic system weight
W_HYD = .001*W_o # hydrolic
print("Raymer W_HYD = ", W_HYD)
# ---------------------------------------------------------------------------------------------------------------
# avionic System installed
W_UAV = 100 # weight of avionic system uninstalled
W_AV = 2.117*(W_UAV**.933)
print("both W_AV = ", W_AV)
# ----------------------------------------------------------------------------------------------------------------
# Electrical System
W_EL = 12.57*((W_FS+W_AV)**.51)
print("both W_EL =", W_EL)
# -------------------------------------------------------------------------------------------------------------------
# Air-conditioning and anti-icing systems
N_OCC = 5 # number of occupants
v_sound = 767.269 # @ S-L in mph
M = (V_H*1.1)/v_sound
W_AC = .265*(W_o**.52)*(N_OCC**.68)*(W_AV**.17)*(M**.08)
print("both W_AC = ", W_AC)
# ------------------------------------------------------------------------------------------------------------------
# Furnishings
N_crew = 1
q_H = .5*((180*1.1)**2)*roe # lbf/ft^2
W_FURN = .0582*W_o-65
print("Raymer W_FURN = ", W_FURN)

W_FURN1 = 34.5*N_crew*(q_H**.25)
print("Nicolai W_FURN = ", W_FURN1)
# ----------------------------------------------------------------------------------------------------------------


