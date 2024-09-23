import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# System Parameters
m1, m2 = 1.0, 1.0
l1, l2 = 1.0, 1.0
g = 9.81
theta_d1, theta_d2 = np.pi / 2, np.pi / 2
lambda1, lambda2 = 15, 15
K1, K2 = 100, 60

# Dynamics function (same as before)
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

# Control law with properly defined M matrix
def sliding_mode_control(theta, theta_dot, theta_d, theta_ddot_d):
    # Tracking error
    e = theta - theta_d
    e_dot = theta_dot
    
    # Sliding surfaces
    S1 = e_dot[0] + lambda1 * e[0]
    S2 = e_dot[1] + lambda2 * e[1]
    
    # Calculate M matrix (inertia matrix) based on current theta values
    A1 = (m1 + m2) * l1**2
    A2 = m2 * l1 * l2 * np.cos(theta[0] - theta[1])
    A1_prime = m2 * l2**2
    M = np.array([[A1, A2], [A2, A1_prime]])

    # Control law (with smoothing to reduce chattering)
    tau1 = M[0, 0] * (theta_ddot_d[0] - lambda1 * e_dot[0]) - K1 * np.sign(S1)
    tau2 = M[1, 1] * (theta_ddot_d[1] - lambda2 * e_dot[1]) - K2 * np.sign(S2)
    
    return np.array([tau1, tau2])

# Simulation function (same as before)
def simulate_smc(initial_state, time_span, dt=0.01):
    n_steps = int(time_span / dt)
    state = np.array(initial_state)
    trajectory = [state]
    
    for step in range(n_steps):
        theta = state[:2]
        theta_dot = state[2:]
        theta_ddot_d = np.array([0.0, 0.0])
        tau = sliding_mode_control(theta, theta_dot, np.array([theta_d1, theta_d2]), theta_ddot_d)
        theta_ddot = dynamics(theta, theta_dot, tau)
        theta_dot_next = theta_dot + theta_ddot * dt
        theta_next = theta + theta_dot * dt
        state = np.concatenate([theta_next, theta_dot_next])
        trajectory.append(state)
    
    return np.array(trajectory)

# Example simulation
initial_state = [0.0, 0.0, 0.0, 0.0]
trajectory = simulate_smc(initial_state, 10)

# Extract angles over time
theta1_vals = trajectory[:, 0]
theta2_vals = trajectory[:, 1]

# Arm position function
def arm_position(theta1, theta2):
    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)
    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)
    return (x1, y1), (x2, y2)

# Plot and animation setup
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

line, = ax.plot([], [], 'o-', lw=2)

# Initialization function for animation
def init():
    line.set_data([], [])
    return line,

# Animation update function
def update(frame):
    theta1 = theta1_vals[frame]
    theta2 = theta2_vals[frame]
    (x1, y1), (x2, y2) = arm_position(theta1, theta2)
    line.set_data([0, x1, x2], [0, y1, y2])
    return line,

# Create animation
ani = FuncAnimation(fig, update, frames=len(theta1_vals), init_func=init, blit=True, interval=50)

# Show animation
plt.grid()
plt.show()
