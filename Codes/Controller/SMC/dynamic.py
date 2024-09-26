import numpy as np
from system_parameters import *

global gg

def dynamics(theta, theta_dot, tau):
    A1 = (m1 + m2) * l1**2
    A2 = m2 * l1 * l2 * np.cos(theta[0] - theta[1])
    A3 = m2 * l1 * l2 * np.sin(theta[0] - theta[1])
    A4 = (m1 + m2) * g * l1 * np.sin(theta[0])
    A1_prime = m2 * l2**2
    A4_prime = m2 * g * l2 * np.sin(theta[1])
    
    M = np.array([[A1, A2], [A2, A1_prime]])
    C = np.array([[0, A3 * theta_dot[1]], [-A3 * theta_dot[0], 0]])
    G = np.array([A4, A4_prime])
    
    theta_ddot = np.linalg.inv(M) @ (tau - C @ theta_dot - G)
    return theta_ddot