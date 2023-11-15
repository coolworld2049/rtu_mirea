import random
import plotly.graph_objects as go
from loguru import logger


def sphere_function(x):
    return sum([val**2 for val in x])


class Bee:
    def __init__(self, num_dimensions):
        self.num_dimensions = num_dimensions
        self.position = [random.uniform(-5, 5) for _ in range(num_dimensions)]
        self.fitness = sphere_function(self.position)

    def update(self, new_position, new_fitness):
        self.position = new_position
        self.fitness = new_fitness

    def generate_random_position(self):
        return [random.uniform(-5, 5) for _ in range(self.num_dimensions)]


class ABCAlgorithm:
    def __init__(self, num_employed, num_onlookers, max_iterations, num_dimensions=2):
        self.probabilities = None
        self.num_employed = num_employed
        self.num_onlookers = num_onlookers
        self.max_iterations = max_iterations
        self.num_dimensions = num_dimensions

        self.employed_bees = [Bee(num_dimensions) for _ in range(num_employed)]
        self.best_solution = min(self.employed_bees, key=lambda bee: bee.fitness)

        # Lists for storing fitness values for visualization
        self.fitness_values = []
        self.best_fitness_values = []

    def run_algorithm(self):
        for iteration in range(self.max_iterations):
            self.employed_bees_phase()
            self.calculate_probabilities()
            self.onlooker_bees_phase()
            self.scout_bees_phase()

            self.fitness_values.append(self.best_solution.fitness)
            self.best_fitness_values.append(self.best_solution.fitness)

            logger.info(
                f"Iteration {iteration}: Best Fitness = {self.best_solution.fitness}"
            )

        return self.best_solution, self.fitness_values, self.best_fitness_values

    def employed_bees_phase(self):
        for bee in self.employed_bees:
            neighbor_bee = random.choice(self.employed_bees)
            while neighbor_bee is bee:
                neighbor_bee = random.choice(self.employed_bees)

            new_position = [
                bee.position[i]
                + random.uniform(-1, 1) * (bee.position[i] - neighbor_bee.position[i])
                for i in range(self.num_dimensions)
            ]
            new_fitness = sphere_function(new_position)

            if new_fitness < bee.fitness:
                bee.update(new_position, new_fitness)

    def calculate_probabilities(self):
        total_fitness = sum(bee.fitness for bee in self.employed_bees)
        self.probabilities = [bee.fitness / total_fitness for bee in self.employed_bees]

    def onlooker_bees_phase(self):
        for _ in range(self.num_onlookers):
            selected_bee = random.choices(self.employed_bees, self.probabilities)[0]

            neighbor_bee = random.choice(self.employed_bees)
            while neighbor_bee is selected_bee:
                neighbor_bee = random.choice(self.employed_bees)

            new_position = [
                selected_bee.position[i]
                + random.uniform(-1, 1)
                * (selected_bee.position[i] - neighbor_bee.position[i])
                for i in range(self.num_dimensions)
            ]
            new_fitness = sphere_function(new_position)

            if new_fitness < selected_bee.fitness:
                selected_bee.update(new_position, new_fitness)

    def scout_bees_phase(self):
        for bee in self.employed_bees:
            if bee.fitness > self.best_solution.fitness:
                self.best_solution = bee


def plot_fitness_progression_plotly(iterations, fitness_values, best_fitness_values):
    # Plot fitness values over iterations using plotly
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=fitness_values,
            mode="lines",
            name="Fitness of Employed Bees",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=iterations, y=best_fitness_values, mode="lines", name="Best Fitness"
        )
    )

    fig.update_layout(
        title="ABC Algorithm - Fitness Progression",
        xaxis_title="Iteration",
        yaxis_title="Fitness",
        legend=dict(x=0, y=1),
        template="plotly_dark",
    )

    fig.show()


if __name__ == "__main__":
    num_employed = 40
    num_onlookers = 10
    max_iterations = 30

    abc_algorithm = ABCAlgorithm(num_employed, num_onlookers, max_iterations)
    best_solution, fitness_values, best_fitness_values = abc_algorithm.run_algorithm()
    logger.info(
        f"Best solution found at position {best_solution.position} with fitness {best_solution.fitness}"
    )

    iterations = list(range(max_iterations))
    plot_fitness_progression_plotly(iterations, fitness_values, best_fitness_values)
