import math
import random
import matplotlib.pyplot as plt
from loguru import logger
from matplotlib.animation import FuncAnimation

random.seed(42)


class FitnessFunction:
    @staticmethod
    def rastrigin_function(x):
        A = 10
        return A * len(x) + sum(
            [(val**2 - A * math.cos(2 * math.pi * val)) for val in x]
        )


class Bee:
    def __init__(self, num_dimensions, fitness_function):
        # Инициализация пчелы со случайной позицией и вычислением её фитнес-функции
        self.num_dimensions = num_dimensions
        self.position = [random.uniform(-5, 5) for _ in range(num_dimensions)]
        self.fitness_function = fitness_function
        self.fitness = fitness_function.rastrigin_function(self.position)

    def update(self, new_position, new_fitness):
        self.position = new_position
        self.fitness = new_fitness

    def generate_random_position(self):
        return [random.uniform(-5, 5) for _ in range(self.num_dimensions)]


class ABCAlgorithm:
    def __init__(
        self,
        num_employed,
        num_onlookers,
        max_iterations,
        fitness_function,
        num_dimensions=2,
    ):
        self.fitness_function = fitness_function
        self.probabilities = None
        self.num_employed = num_employed
        self.num_onlookers = num_onlookers
        self.max_iterations = max_iterations
        self.num_dimensions = num_dimensions
        self.employed_bees = [
            Bee(num_dimensions, self.fitness_function) for _ in range(num_employed)
        ]
        self.best_solution = min(self.employed_bees, key=lambda bee: bee.fitness)
        self.fitness_values = []
        self.best_fitness_values = []

    def run(self):
        """
        Использование различных типов пчёл позволяет алгоритму достичь
        баланса между интенсивным исследованием локальных областей и способностью выхода из локальных минимумов,
        что может быть критично для глобальной оптимизации.
        """
        employed_bees_positions = []
        for iteration in range(self.max_iterations):
            self.employed_bees_phase()
            employed_bees_positions.append([bee.position for bee in self.employed_bees])

            total_fitness = sum(bee.fitness for bee in self.employed_bees)
            self.probabilities = [
                bee.fitness / total_fitness for bee in self.employed_bees
            ]
            self.onlooker_bees_phase()
            self.scout_bees_phase()
            self.fitness_values.append([bee.fitness for bee in self.employed_bees])
            self.best_fitness_values.append(
                (self.best_solution.position, self.best_solution.fitness)
            )
            logger.info(
                f"Iteration {iteration}: Best Fitness = {self.best_solution.fitness}"
            )

        return (
            self.best_solution,
            self.fitness_values,
            self.best_fitness_values,
            employed_bees_positions,
        )

    def employed_bees_phase(self):
        """
        - Трудовые пчёлы ответственны за исследование окрестности своих
            текущих позиций в пространстве параметров.
        - Каждая трудовая пчела выбирает случайного соседа из числа трудовых пчёл
            и обновляет свою позицию на основе позиции выбранной пчелы.
        - Если новая позиция обеспечивает улучшение (меньшее значение фитнес-функции),
            то трудовая пчела обновляет свою позицию.
        """
        for bee in self.employed_bees:
            neighbor_bee = random.choice(self.employed_bees)
            while neighbor_bee is bee:
                neighbor_bee = random.choice(self.employed_bees)
            new_position = self.update_position(bee.position, neighbor_bee.position)
            new_fitness = self.fitness_function.rastrigin_function(new_position)
            if new_fitness < bee.fitness:
                bee.update(new_position, new_fitness)

    def onlooker_bees_phase(self):
        """
        - Наблюдатели следят за трудовыми пчёлами и выбирают пчелу для наблюдения
            с вероятностью, пропорциональной их фитнес-значениям.
        - Как и трудовые пчёлы, наблюдатели обновляют свои позиции,
            основываясь на выбранной трудовой пчеле и её соседе.
        - Так же как и в случае с трудовыми пчёлами, если новая позиция обеспечивает улучшение,
            то наблюдатель обновляет свою позицию.
        """
        for _ in range(self.num_onlookers):
            selected_bee = random.choices(self.employed_bees, self.probabilities)[0]
            neighbor_bee = random.choice(self.employed_bees)
            while neighbor_bee is selected_bee:
                neighbor_bee = random.choice(self.employed_bees)
            new_position = self.update_position(
                selected_bee.position, neighbor_bee.position
            )
            new_fitness = self.fitness_function.rastrigin_function(new_position)
            if new_fitness < selected_bee.fitness:
                selected_bee.update(new_position, new_fitness)

    def scout_bees_phase(self):
        """
        - Разведчики проверяют, необходимо ли заменить текущего лучшего решение.
        - Если какая-то трудовая пчела имеет фитнес-значение лучше, чем у текущего лучшего решения,
            то это становится новым лучшим решением.
        """
        for bee in self.employed_bees:
            if bee.fitness > self.best_solution.fitness:
                self.best_solution = bee

    def update_position(self, current_position, neighbor_position):
        return [
            current_position[i]
            + random.uniform(-1, 1) * (current_position[i] - neighbor_position[i])
            for i in range(self.num_dimensions)
        ]


def plot_fitness_progression_matplotlib(
    iterations, fitness_values, best_fitness_values, employed_bees_positions
):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    def update_plot(iteration):
        ax.clear()
        ax.set_title(f"Iteration {iteration}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Fitness")

        for i, positions in enumerate(employed_bees_positions[iteration]):
            ax.scatter(
                positions[0],
                positions[1],
                fitness_values[iteration][i],
                c="b",
                marker="o",
            )

        best_position = best_fitness_values[iteration][0]
        best_fitness = best_fitness_values[iteration][1]
        ax.scatter(
            best_position[0],
            best_position[1],
            best_fitness,
            c="r",
            marker="o",
            s=40,
            label="Best solution value",
        )
        ax.legend()

        return (ax,)

    ani = FuncAnimation(fig, update_plot, frames=iterations, repeat=False)
    plt.show()


if __name__ == "__main__":
    num_employed = 40
    num_onlookers = 20
    max_iterations = 91
    abc_algorithm = ABCAlgorithm(
        num_employed=num_employed,
        num_onlookers=num_onlookers,
        max_iterations=max_iterations,
        fitness_function=FitnessFunction(),
        num_dimensions=2,
    )
    (
        best_solution,
        fitness_values,
        best_fitness_values,
        employed_bees_positions,
    ) = abc_algorithm.run()

    logger.info(
        f"Best solution found at position {best_solution.position} with fitness {best_solution.fitness}"
    )

    iterations = list(range(max_iterations))
    # plot_fitness_progression_matplotlib(
    #     iterations, fitness_values, best_fitness_values, employed_bees_positions
    # )
