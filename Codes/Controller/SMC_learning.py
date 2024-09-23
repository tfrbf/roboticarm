import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# System parameters
a = 1       # System coefficient a
b = 2       # System coefficient b
lambda_ = 5  # Sliding surface parameter
k = 1       # Sliding control gain

# Desired state
x_d = 80     # Desired value of x(t)

# Sliding Mode Control system dynamics
def smc_system(t, x):
    # Error calculation
    e = x[0] - x_d
    
    # Sliding surface definition
    s = lambda_ * e + a * x[0]
    
    # Equivalent control
    u_eq = -(a * x[0] + lambda_ * e) / b
    
    # Sliding control
    u_s = -k * np.sign(s)
    
    # Total control input
    u = u_eq + u_s
    
    # System dynamics (dx/dt)
    dxdt = a * x[0] + b * u 
    return [dxdt]

# Simulation time
t_span = (0, 10)  # Time span for simulation
x0 = [5]          # Initial condition

# Solve the system using solve_ivp
sol = solve_ivp(smc_system, t_span, x0, t_eval=np.linspace(0, 10, 1000))

# Plotting the results
plt.plot(sol.t, sol.y[0], label='x(t)', linewidth=2)
plt.plot(sol.t, x_d * np.ones_like(sol.t), '--r', label='x_d(t)', linewidth=2)
plt.title('Sliding Mode Control for First-Order System')
plt.xlabel('Time (s)')
plt.ylabel('State x(t)')
plt.legend()
plt.grid(True)
plt.show()

