import numpy as np


def charged_system_search(
    obj_func, dim, num_agents, iterations, lower_bound, upper_bound
):
    """
    Charged System Search algorithm implementation.

    Parameters:
    - obj_func: Objective function to be minimized
    - dim: Dimension of the search space
    - num_agents: Number of charged particles (agents)
    - iterations: Number of iterations
    - lower_bound: Lower bound of the search space
    - upper_bound: Upper bound of the search space

    Returns:
    - best_position: Best solution found
    - best_fitness: Fitness value of the best solution
    """

    # Initialize positions and charges
    positions = np.random.uniform(lower_bound, upper_bound, (num_agents, dim))
    charges = np.random.uniform(-1, 1, num_agents)

    # Main loop
    for _ in range(iterations):
        # Evaluate fitness for each agent
        fitness_values = np.array([obj_func(position) for position in positions])

        # Find the index of the agent with the best fitness
        best_index = np.argmin(fitness_values)
        best_position = positions[best_index]
        best_fitness = fitness_values[best_index]

        # Update charges
        charges = charges * np.exp(-fitness_values)

        # Update positions using charged particle movement equation
        for i in range(num_agents):
            for j in range(dim):
                rand1, rand2 = np.random.rand(), np.random.rand()
                positions[i, j] = (
                    best_position[j] + rand1 * (upper_bound - lower_bound) * charges[i]
                )
                positions[i, j] = max(lower_bound, min(upper_bound, positions[i, j]))

    return best_position, best_fitness


# Example usage:
def objective_function(x):
    # Example objective function (minimize)
    return np.sum(x**2)


# Parameters
dimension = 5
num_particles = 20
num_iterations = 100
lower_bound = -5.0
upper_bound = 5.0

# Run Charged System Search
best_solution, best_fitness = charged_system_search(
    objective_function,
    dimension,
    num_particles,
    num_iterations,
    lower_bound,
    upper_bound,
)

# Print results
print("Best Solution:", best_solution)
print("Best Fitness:", best_fitness)
