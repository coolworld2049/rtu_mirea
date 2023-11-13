import random
import matplotlib.pyplot as plt
from typing import Callable


class Particle:
    def __init__(self, num_dimensions):
        self.position = [random.uniform(-5, 5) for _ in range(num_dimensions)]
        self.velocity = [random.uniform(-1, 1) for _ in range(num_dimensions)]
        self.personal_best = self.position


class PSOAlgorithm:
    def __init__(
        self,
        num_particles,
        num_dimensions,
        max_iterations,
        c1,
        c2,
        w,
        fitness_function: Callable,
    ):
        self.num_particles = num_particles
        self.num_dimensions = num_dimensions
        self.max_iterations = max_iterations
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.fitness_function = fitness_function
        self.particles = [Particle(num_dimensions) for _ in range(num_particles)]
        self.global_best = self.particles[0].position
        self.global_best_value = self.fitness_function(*self.global_best)

    def optimize(self):
        best_values = []

        for iteration in range(self.max_iterations):
            for particle in self.particles:
                x, y = particle.position
                current_fitness = self.fitness_function(x, y)

                if current_fitness < self.fitness_function(*particle.personal_best):
                    particle.personal_best = particle.position

                if current_fitness < self.global_best_value:
                    self.global_best = particle.position
                    self.global_best_value = current_fitness

                for i in range(self.num_dimensions):
                    r1 = random.random()
                    r2 = random.random()
                    cognitive = (
                        self.c1
                        * r1
                        * (particle.personal_best[i] - particle.position[i])
                    )
                    social = self.c2 * r2 * (self.global_best[i] - particle.position[i])
                    particle.velocity[i] = (
                        self.w * particle.velocity[i] + cognitive + social
                    )
                    particle.position[i] = particle.position[i] + particle.velocity[i]

            best_values.append(self.global_best_value)
            self.visualize(iteration, best_values)

        print("Optimal solution:", self.global_best)
        print("Optimal value:", self.global_best_value)

    def visualize(self, iteration, best_values):
        plt.clf()
        plt.plot(best_values)
        plt.title(f"Iteration {iteration + 1}: Best Value = {self.global_best_value}")
        plt.xlabel("Iteration")
        plt.ylabel("Best Value")
        plt.pause(0.01)


if __name__ == "__main__":
    num_particles = 20
    num_dimensions = 2
    max_iterations = 100
    c1 = 2.0
    c2 = 2.0
    w = 0.7

    # Define the Himmelblau function as a fitness function
    def himmelblau(x, y):
        return (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2

    pso = PSOAlgorithm(
        num_particles, num_dimensions, max_iterations, c1, c2, w, himmelblau
    )
    pso.optimize()

    # Show the final plot
    plt.show()
