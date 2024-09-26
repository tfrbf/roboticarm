import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import controller
import dynamic
from system_parameters import *


# Simulation function
def simulate_smc(initial_state, time_span, dt=0.01):
    n_steps = int(time_span / dt)
    state = np.array(initial_state)
    trajectory = [state]
    sliding_surface_values = []

    for step in range(n_steps):
        theta = state[:2]
        theta_dot = state[2:]
        tau, S1, S2 = controller.sliding_mode_control(theta, theta_dot, np.array([theta_d1, theta_d2]))
        theta_ddot = dynamic.dynamics(theta, theta_dot, tau)
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






# Time vector
time = np.linspace(0, 10, len(theta1_vals))

# Plot angles (θ1, θ2)
plt.figure(figsize=(8, 6))
plt.plot(time, theta1_vals, label=r'$\theta_1$ (actual)', color='b')
plt.plot(time, np.full_like(time, theta_d1), '--', label=r'$\theta_1$ (desired)', color='r')
plt.plot(time, theta2_vals, label=r'$\theta_2$ (actual)', color='g')
plt.plot(time, np.full_like(time, theta_d2), '--', label=r'$\theta_2$ (desired)', color='orange')
plt.title('Joint Angles Over Time')
plt.xlabel('Time [s]')
plt.ylabel('Angle [rad]')
plt.legend()
plt.grid(True)


# Compute sliding surfaces over time
S1_vals = np.gradient(theta1_vals) + lambda1 * (theta1_vals - theta_d1)
S2_vals = np.gradient(theta2_vals) + lambda2 * (theta2_vals - theta_d2)

# Compute Lyapunov function V over time
V_vals = 0.5 * (S1_vals**2 + S2_vals**2)

# Plot Lyapunov function
plt.figure(figsize=(8, 6))
plt.plot(time, V_vals, label='Lyapunov Function $V(t)$', color='purple')
plt.title('Lyapunov Function Over Time')
plt.xlabel('Time [s]')
plt.ylabel('Lyapunov Function $V$')
plt.grid(True)
plt.legend()




# Show the plot
plt.tight_layout()
plt.show()
