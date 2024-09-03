# %%
import numpy as np
from scipy.optimize import fsolve

# Define the equation to solve
def obj(p_c, gamma, k_min):
    s = p_c ** ((2-gamma)/(1-gamma)) - (2 + (2 - gamma) / (3 - gamma) * k_min * (p_c**((3 - gamma) / (1 - gamma)) - 1))
    return s ** 2

import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Parameters
gamma_values = np.linspace(2.1, 8.0, 400)  # Range of gamma values
k_min = 3    # Example value for k_min

# Initial guess for p_c
initial_guess = 0.5

# Solve the equation for each gamma value
p_c_solutions = []
for gamma in gamma_values:
    res = minimize(obj, bounds = [(0, 1)], x0 = [initial_guess], args = (gamma, k_min))
    p_c_solutions.append(res.x[0])
    print(obj(res.x[0], gamma, k_min))

# %%
# Plot the results
plt.plot(gamma_values, p_c_solutions, label='Critical point p_c')
plt.xlabel('Gamma')
plt.ylabel('Critical point p_c')
plt.title('Critical point p_c as a function of Gamma')
plt.legend()
# %%
