import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# System Parameters
m1, m2 = 1.0, 1.0
l1, l2 = 1.0, 1.0
g = 9.81
theta_d1, theta_d2 = np.pi / 2, np.pi / 2  # Desired angles
lambda1, lambda2 = 15, 15
K1, K2 = 100, 60

# Dynamics function
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

# Control law
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

# Simulation function
def simulate_smc(initial_state, time_span, dt=0.01):
    n_steps = int(time_span / dt)
    state = np.array(initial_state)
    trajectory = [state]
    sliding_surface_values = []

    for step in range(n_steps):
        theta = state[:2]
        theta_dot = state[2:]
        tau, S1, S2 = sliding_mode_control(theta, theta_dot, np.array([theta_d1, theta_d2]))
        theta_ddot = dynamics(theta, theta_dot, tau)
        theta_dot_next = theta_dot + theta_ddot * dt
        theta_next = theta + theta_dot * dt
        state = np.concatenate([theta_next, theta_dot_next])
        trajectory.append(state)
        
        # Store sliding surfaces for visualization
        sliding_surface_values.append((S1, S2))
    
    return np.array(trajectory), np.array(sliding_surface_values)

# Example simulation
initial_state = [0.0, 0.0, 0.0, 0.0]
trajectory, sliding_surface_values = simulate_smc(initial_state, 10)

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
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# Arm plot setup
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
line, = ax1.plot([], [], 'o-', lw=2)
desired_marker1, = ax1.plot([], [], 'go', label='Desired Angle 1')
desired_marker2, = ax1.plot([], [], 'go', label='Desired Angle 2')
actual_marker1, = ax1.plot([], [], 'ro', label='Actual Angle 1')
actual_marker2, = ax1.plot([], [], 'ro', label='Actual Angle 2')
ax1.legend()
ax1.set_title("2D Visualization of Two-Link Robotic Arm")

# Sliding surface plot setup
ax2.set_xlim(0, len(theta1_vals))
ax2.set_ylim(-10, 10)
sliding_surface_line1, = ax2.plot([], [], 'b-', label='Sliding Surface S1')
sliding_surface_line2, = ax2.plot([], [], 'r-', label='Sliding Surface S2')
ax2.legend()
ax2.set_title("Sliding Surfaces")

# Initialization function for animation
def init():
    line.set_data([], [])
    desired_marker1.set_data([], [])
    desired_marker2.set_data([], [])
    actual_marker1.set_data([], [])
    actual_marker2.set_data([], [])
    
    sliding_surface_line1.set_data([], [])
    sliding_surface_line2.set_data([], [])
    
    return (line, desired_marker1, desired_marker2, actual_marker1, actual_marker2, 
            sliding_surface_line1, sliding_surface_line2)

# Animation update function
def update(frame):
    theta1 = theta1_vals[frame]
    theta2 = theta2_vals[frame]
    (x1, y1), (x2, y2) = arm_position(theta1, theta2)
    line.set_data([0, x1, x2], [0, y1, y2])
    
    # Update desired angles
    desired_marker1.set_data([0, l1 * np.sin(theta_d1)], [-l1 * np.cos(theta_d1), -l1 * np.cos(theta_d1)])
    desired_marker2.set_data([x1, x1 + l2 * np.sin(theta_d2)], [y1, y1 - l2 * np.cos(theta_d2)])

    # Update actual angles
    actual_marker1.set_data([0, x1], [0, y1])
    actual_marker2.set_data([x1, x2], [y1, y2])
    
    # Update sliding surfaces
    S1, S2 = sliding_surface_values[frame]
    sliding_surface_line1.set_data(range(frame + 1), [s[0] for s in sliding_surface_values[:frame + 1]])
    sliding_surface_line2.set_data(range(frame + 1), [s[1] for s in sliding_surface_values[:frame + 1]])

    return (line, desired_marker1, desired_marker2, actual_marker1, actual_marker2, 
            sliding_surface_line1, sliding_surface_line2)

# Create animation
ani = FuncAnimation(fig, update, frames=len(theta1_vals), init_func=init, blit=True, interval=50)

# Show animation
plt.tight_layout()
plt.show()
