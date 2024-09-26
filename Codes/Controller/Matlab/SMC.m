% Sliding Mode Control for a First-Order System

% System parameters
a = 1;     % System coefficient a
b = 2;     % System coefficient b
lambda = 7;  % Sliding surface parameter
k = 7;     % Sliding control gain

% Desired state
x_d = 50;   % Desired value of x(t)

% Simulation parameters
tspan = [0 30];  % Time span for simulation
x0 = 5;          % Initial condition

% Sliding Mode Control function
[t, x] = ode45(@(t, x) smc_system(t, x, x_d, a, b, lambda, k), tspan, x0);

% Plotting the results
figure;
plot(t, x, 'LineWidth', 2);
hold on;
plot(t, x_d * ones(size(t)), '--r', 'LineWidth', 2);  % Plot desired state
title('Sliding Mode Control for First-Order System');
xlabel('Time (s)');
ylabel('State x(t)');
legend('x(t)', 'x_d(t)');
grid on;

% SMC function definition
function dxdt = smc_system(t, x, x_d, a, b, lambda, k)
    % Error calculation
    e = x - x_d;
    
    % Sliding surface definition
    s = lambda * e + (a * x);
    
    % Equivalent control
    u_eq = -(a * x + lambda * e) / b;
    
    % Sliding control
    u_s = -k * sign(s);
    
    % Total control input
    u = u_eq + u_s;
    
    % System dynamics
    dxdt = a * x + b * u;
end
