import numpy as np


class ChargedSystemSearch:
    def __init__(self, obj_func, dim, num_agents, iterations, lower_bound, upper_bound):
        self.obj_func = obj_func
        self.dim = dim
        self.num_agents = num_agents
        self.iterations = iterations
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def run(self):
        positions = np.random.uniform(
            self.lower_bound, self.upper_bound, (self.num_agents, self.dim)
        )
        charges = np.random.uniform(-1, 1, self.num_agents)

        for _ in range(self.iterations):
            fitness_values = np.array(
                [self.obj_func(position) for position in positions]
            )
            best_index = np.argmin(fitness_values)
            best_position = positions[best_index]
            best_fitness = fitness_values[best_index]

            charges = charges * np.exp(-fitness_values)

            for i in range(self.num_agents):
                for j in range(self.dim):
                    rand1, rand2 = np.random.rand(), np.random.rand()
                    positions[i, j] = (
                        best_position[j]
                        + rand1 * (self.upper_bound - self.lower_bound) * charges[i]
                    )
                    positions[i, j] = max(
                        self.lower_bound, min(self.upper_bound, positions[i, j])
                    )

        return best_position, best_fitness


# Example usage:
def objective_function(x):
    return x[0] ** 2 + x[1] ** 2


def sphere_function(x):
    return np.sum(x**2)


def rosenbrock_function(x):
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2)


def rastrigin_function(x):
    A = 10
    return A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x))


dimension = 2
num_particles = 20
num_iterations = 10
lower_bound = -5.0
upper_bound = 5.0

css = ChargedSystemSearch(
    objective_function,
    dimension,
    num_particles,
    num_iterations,
    lower_bound,
    upper_bound,
)
best_solution, best_fitness = css.run()

print("Best Solution:", best_solution)
print("Best Fitness:", best_fitness)
