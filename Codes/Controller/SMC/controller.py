import numpy as np
from system_parameters import *

def sliding_mode_control(theta, theta_dot, theta_d):
    # Tracking error
    e = theta - theta_d
    e_dot = theta_dot
    
    # Sliding surfaces
    S1 = e_dot[0] + lambda1 * e[0]
    S2 = e_dot[1] + lambda2 * e[1]
    
    # Calculate M matrix (inertia matrix)
    A1 = (m1 + m2) * l1**2
    A2 = m2 * l1 * l2 * np.cos(theta[0] - theta[1])
    A1_prime = m2 * l2**2
    M = np.array([[A1, A2], [A2, A1_prime]])

    # Control law
    tau1 = M[0, 0] * (0 - lambda1 * e_dot[0]) - K1 * np.sign(S1)
    tau2 = M[1, 1] * (0 - lambda2 * e_dot[1]) - K2 * np.sign(S2)
    
    return np.array([tau1, tau2]), S1, S2