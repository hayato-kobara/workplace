import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import nafusion_utils as na
na.set_style()

# Constants for Argon
A = 13.6  # (cm*Torr)^-1
B = 235 # V/(cm*Torr)
gamma = 0.01 

# Paschen curve equation
def paschen_voltage(pd, A, B, gamma):
    return (B * pd) / (np.log(A * pd) - np.log(np.log(1 + 1/gamma)))

# For finding minimum
def objective(pd):
    return paschen_voltage(pd[0], A, B, gamma)

# Initial guess for pd
pd_guess = [1.0]
res = minimize(objective, pd_guess, bounds=[(0.1, 100)])

pd_min = res.x[0]
V_min = res.fun

pd_values = np.logspace(-1, 2, 1000)
V_values = paschen_voltage(pd_values, A, B, gamma)

# Let's verify with analytical minimum
# V = B*pd / (ln(A*pd) - C) where C = ln(ln(1+1/gamma))
# dV/d(pd) = 0 -> ln(A*pd) - C - 1 = 0 -> ln(A*pd) = C + 1
# pd_min_analytical = exp(C+1) / A
C = np.log(np.log(1 + 1/gamma))
pd_min_analytical = np.exp(C + 1) / A
V_min_analytical = paschen_voltage(pd_min_analytical, A, B, gamma)

plt.figure(figsize=(8, 6))
plt.plot(pd_values, V_values, label=f'Paschen Curve for Ar ($\gamma$={gamma})')
plt.scatter([pd_min_analytical], [V_min_analytical], color='red', zorder=5, label=f'Minimum: pd={pd_min_analytical:.2f}, V={V_min_analytical:.1f}')
plt.xlabel('Pressure $\\times$ Distance ($pd$) [Torr$\\cdot$cm]')
plt.ylabel('Breakdown Voltage ($V$) [V]')
plt.title('Paschen Curve for Argon')
plt.xscale('log')
plt.yscale('log')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('paschen_argon.png')
plt.show()
print(f"pd_min_num={pd_min}, V_min_num={V_min}")
print(f"pd_min_ana={pd_min_analytical}, V_min_ana={V_min_analytical}")