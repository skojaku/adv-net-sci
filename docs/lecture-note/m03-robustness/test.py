# %%
import numpy as np
from scipy.optimize import fsolve

n = 12
m = 20

def obj(x):
    score  = n * x * (n-1) + n * x * n * (1-x) - 2 * m
    return score **2

res = fsolve(obj, 0.1)
print(res)


# %%
