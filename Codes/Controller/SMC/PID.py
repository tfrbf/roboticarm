import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the lengths of the links
L1 = 1.0  # Length of the first link
L2 = 1.0  # Length of the second link

# Define PID control parameters
Kp = 2.0  # Proportional gain
Ki = 0.01  # Integral gain
Kd = 0.1  # Derivative gain

# Initialize PID control variables
previous_error1 = 0
integral1 = 0
previous_error2 = 0
integral2 = 0

def forward_kinematics(theta1, theta2):
    """
    Compute the (x, y) coordinates of the end effector given joint angles theta1 and theta2.
    """
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    
    x2 = x1 + L2 * np.cos(theta1 + theta2)
    y2 = y1 + L2 * np.sin(theta1 + theta2)
    
    return (x1, y1), (x2, y2)

def pid_control(target, current, previous_error, integral, dt):
    """
    A basic PID controller that calculates the control action based on error.
    """
    # Error between the target and current angle
    error = target - current
    
    # Proportional term
    P = Kp * error
    
    # Integral term
    integral += error * dt
    I = Ki * integral
    
    # Derivative term
    derivative = (error - previous_error) / dt
    D = Kd * derivative
    
    # PID output
    output = P + I + D
    
    return output, error, integral

# Initialize figure and axis
fig, ax = plt.subplots()
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_aspect('equal')
plt.title('2 DOF Robotic Arm with PID Control')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)

# Initialize the lines that will represent the arm
line, = ax.plot([], [], marker='o')

# Initial joint angles (in radians)
theta1 = np.pi / 8  # 45 degrees
theta2 = np.pi / 8 # 45 degrees

# Define target angles for the joints (desired positions)
target_theta1 = np.pi / 2 # Desired angle for joint 1
target_theta2 = np.pi / 2  # Desired angle for joint 2

# Function to initialize the animation
def init():
    line.set_data([], [])
    return line,

# Function to update the frame in the animation
def update(frame):
    global theta1, theta2, previous_error1, integral1, previous_error2, integral2
    
    # Time step (assume constant for simplicity)
    dt = 0.1
    
    # Apply PID control to joint 1
    control1, error1, integral1 = pid_control(target_theta1, theta1, previous_error1, integral1, dt)
    previous_error1 = error1
    
    # Apply PID control to joint 2
    control2, error2, integral2 = pid_control(target_theta2, theta2, previous_error2, integral2, dt)
    previous_error2 = error2
    
    # Update the joint angles with the control action
    theta1 += control1 * dt
    theta2 += control2 * dt
    
    # Get the positions of the joints
    joint1, end_effector = forward_kinematics(theta1, theta2)

    # Update the line data for the plot
    line.set_data([0, joint1[0], end_effector[0]], [0, joint1[1], end_effector[1]])
    return line,

# Create animation object
ani = FuncAnimation(fig, update, frames=np.arange(0, 200), init_func=init, blit=True, interval=50)

# Show the animation
plt.show()
