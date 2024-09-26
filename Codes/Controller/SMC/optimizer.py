import numpy as np
import random
from dynamic import *
from controller import *


# Genetic Algorithm parameters
population_size = 20
generations = 50
mutation_rate = 0.05
lambda_bounds = (10, 100)
K_bounds = (10, 100)

# Fitness function (Objective function) to minimize tracking error
def fitness(params):
    lambda1, lambda2, K1, K2 = params
    m1, m2 = 1.0, 1.0
    l1, l2 = 1.0, 1.0
    theta_d1, theta_d2 = np.pi / 2, np.pi / 3  # Desired angles
    
    # Initialize state [theta1, theta2, theta_dot1, theta_dot2]
    initial_state = np.array([0.0, 0.0, 0.0, 0.0])

    # Time parameters for simulation
    time_span = 10  # Total simulation time
    dt = 0.01       # Time step

    # Simulation loop
    n_steps = int(time_span / dt)
    state = initial_state
    total_error = 0
    
    for step in range(n_steps):
        theta = state[:2]
        theta_dot = state[2:]
        
        # Control torque using sliding mode control
        tau, S1, S2 = sliding_mode_control(theta, theta_dot, np.array([theta_d1, theta_d2]), 
                                           lambda1, lambda2, K1, K2, m1, m2, l1, l2)
        
        # Compute the new accelerations
        theta_ddot = dynamics(theta, theta_dot, tau)
        
        # Euler integration for next state
        theta_dot_next = theta_dot + theta_ddot * dt
        theta_next = theta + theta_dot * dt
        state = np.concatenate([theta_next, theta_dot_next])
        
        # Compute tracking error (squared error between actual and desired angles)
        error = (theta_d1 - theta[0])**2 + (theta_d2 - theta[1])**2
        total_error += error
        
    return total_error

# Random initialization of population
def initialize_population(size):
    return np.array([[random.uniform(*lambda_bounds), random.uniform(*lambda_bounds), 
                      random.uniform(*K_bounds), random.uniform(*K_bounds)] for _ in range(size)])

# Crossover between two parents
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
    child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
    return child1, child2

# Mutation operation
def mutate(individual, mutation_rate=mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            if i < 2:  # Mutate lambda values
                individual[i] = random.uniform(*lambda_bounds)
            else:  # Mutate K values
                individual[i] = random.uniform(*K_bounds)
    return individual

# Genetic Algorithm main loop
def genetic_algorithm():
    population = initialize_population(population_size)
    best_individual = None
    best_fitness = float('inf')

    for gen in range(generations):
        # Evaluate fitness for the population
        fitness_values = np.array([fitness(individual) for individual in population])
        
        # Select the best individual
        gen_best_fitness = np.min(fitness_values)
        gen_best_individual = population[np.argmin(fitness_values)]
        
        if gen_best_fitness < best_fitness:
            best_fitness = gen_best_fitness
            best_individual = gen_best_individual
        
        print(f"Generation {gen+1}: Best Fitness = {best_fitness}")
        
        # Selection process (Roulette wheel selection or tournament)
        selected_population = population[np.argsort(fitness_values)][:population_size//2]
        
        # Crossover and create new generation
        new_population = []
        while len(new_population) < population_size:
            parents = random.sample(list(selected_population), 2)
            child1, child2 = crossover(parents[0], parents[1])
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        
        population = np.array(new_population[:population_size])
    
    return best_individual, best_fitness

# Run the genetic algorithm
best_params, best_error = genetic_algorithm()
print("Best Parameters (lambda1, lambda2, K1, K2):", best_params)
print("Best Error:", best_error)
