import math
import random

from loguru import logger

random.seed(42)


class FitnessFunction:
    @staticmethod
    def rastrigin_function(x):
        A = 10
        return A * len(x) + sum(
            [(val**2 - A * math.cos(2 * math.pi * val)) for val in x]
        )


class Bee:
    def __init__(self, dim, fitness_function):
        self.dim = dim or 2
        self.pos = [random.uniform(-5, 5) for _ in range(dim)]
        self.fitness_function = fitness_function
        self.fitness_value = fitness_function.rastrigin_function(self.pos)

    def update(self, new_pos, new_fitness_value):
        self.pos = new_pos
        self.fitness_value = new_fitness_value

    def generate_random_pos(self):
        return [random.uniform(-5, 5) for _ in range(self.dim)]


class ABCAlgorithm:
    def __init__(
        self,
        num_employed,
        num_onlookers,
        max_iterations,
        fitness_function,
        dim=2,
    ):
        self.fitness_function = fitness_function
        self.probabilities = None
        self.num_employed = num_employed
        self.num_onlookers = num_onlookers
        self.max_iterations = max_iterations
        self.dim = dim
        self.employed_bees = [
            Bee(dim, self.fitness_function) for _ in range(num_employed)
        ]
        self.best_solution = min(self.employed_bees, key=lambda bee: bee.fitness_value)
        self.fitness_values = []
        self.best_fitness_values = []

    def run(self):
        employed_bees_poss = []
        for iteration in range(self.max_iterations):
            self.employed_bees_phase()
            employed_bees_poss.append([bee.pos for bee in self.employed_bees])

            total_fitness = sum(bee.fitness_value for bee in self.employed_bees)
            self.probabilities = [
                bee.fitness_value / total_fitness for bee in self.employed_bees
            ]
            self.onlooker_bees_phase()
            self.local_search_phase()  # Added local search phase
            self.scout_bees_phase()
            self.fitness_values.append(
                [bee.fitness_value for bee in self.employed_bees]
            )
            self.best_fitness_values.append(
                (self.best_solution.pos, self.best_solution.fitness_value)
            )
            logger.info(
                f"Iteration {iteration}: Best Fitness = {self.best_solution.fitness_value}"
            )

        return (
            self.best_solution,
            self.fitness_values,
            self.best_fitness_values,
            employed_bees_poss,
        )

    def employed_bees_phase(self):
        for bee in self.employed_bees:
            neighbor_bee = random.choice(self.employed_bees)
            while neighbor_bee is bee:
                neighbor_bee = random.choice(self.employed_bees)
            new_pos = self.update_pos(bee.pos, neighbor_bee.pos)
            new_fitness = self.fitness_function.rastrigin_function(new_pos)
            if new_fitness < bee.fitness_value:
                bee.update(new_pos, new_fitness)

    def onlooker_bees_phase(self):
        for _ in range(self.num_onlookers):
            selected_bee = random.choices(self.employed_bees, self.probabilities)[0]
            neighbor_bee = random.choice(self.employed_bees)
            while neighbor_bee is selected_bee:
                neighbor_bee = random.choice(self.employed_bees)
            new_pos = self.update_pos(selected_bee.pos, neighbor_bee.pos)
            new_fitness = self.fitness_function.rastrigin_function(new_pos)
            if new_fitness < selected_bee.fitness_value:
                selected_bee.update(new_pos, new_fitness)

    def scout_bees_phase(self):
        for bee in self.employed_bees:
            if bee.fitness_value > self.best_solution.fitness_value:
                self.best_solution = bee

    def local_search_phase(self):
        """
        - Если значение приспособленности лучшего соседа меньше значения приспособленности текущей пчелы,
            это означает, что у соседа есть лучшее решение.
        - Новая позиция генерируется для текущей пчелы с использованием метода update_pos,
            который корректирует позицию на основе разницы между текущей позицией и позицией лучшего соседа.
        - Рассчитывается пригодность новой позиции.
        - Если новая приспособленность лучше текущей,
            положение и приспособленность пчелы обновляются.
        """
        for bee in self.employed_bees:
            best_neighbor = min(
                self.employed_bees,
                key=lambda neighbor: self.fitness_function.rastrigin_function(
                    neighbor.pos
                ),
            )
            if best_neighbor.fitness_value < bee.fitness_value:
                new_pos = self.update_pos(bee.pos, best_neighbor.pos)
                new_fitness = self.fitness_function.rastrigin_function(new_pos)
                if new_fitness < bee.fitness_value:
                    bee.update(new_pos, new_fitness)

    def update_pos(self, current_pos, neighbor_pos):
        return [
            current_pos[i] + random.uniform(-1, 1) * (current_pos[i] - neighbor_pos[i])
            for i in range(self.dim)
        ]


if __name__ == "__main__":
    num_employed = 40
    num_onlookers = 20
    max_iterations = 66
    abc_algorithm = ABCAlgorithm(
        num_employed=num_employed,
        num_onlookers=num_onlookers,
        max_iterations=max_iterations,
        fitness_function=FitnessFunction(),
        dim=2,
    )
    (
        best_solution,
        fitness_values,
        best_fitness_values,
        employed_bees_poss,
    ) = abc_algorithm.run()

    logger.info(
        f"Best solution found at pos {best_solution.pos} with fitness {best_solution.fitness_value}"
    )

    iterations = list(range(max_iterations))
