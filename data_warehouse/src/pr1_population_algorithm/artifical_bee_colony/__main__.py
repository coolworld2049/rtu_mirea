import math
import random
import matplotlib.pyplot as plt
from loguru import logger
from matplotlib.animation import FuncAnimation

random.seed(42)


def rastrigin_function(x):
    A = 10
    return A * len(x) + sum([(val**2 - A * math.cos(2 * math.pi * val)) for val in x])


class Bee:
    def __init__(self, num_dimensions):
        # Инициализация пчелы со случайной позицией и вычислением её фитнес-функции
        self.num_dimensions = num_dimensions
        self.position = [random.uniform(-5, 5) for _ in range(num_dimensions)]
        self.fitness = rastrigin_function(self.position)

    def update(self, new_position, new_fitness):
        # Обновление позиции и фитнес-значения пчелы
        self.position = new_position
        self.fitness = new_fitness

    def generate_random_position(self):
        # Генерация случайной позиции пчелы
        return [random.uniform(-5, 5) for _ in range(self.num_dimensions)]


class ABCAlgorithm:
    def __init__(self, num_employed, num_onlookers, max_iterations, num_dimensions=2):
        # Инициализация параметров и списка трудовых пчел
        self.probabilities = None
        self.num_employed = num_employed
        self.num_onlookers = num_onlookers
        self.max_iterations = max_iterations
        self.num_dimensions = num_dimensions
        self.employed_bees = [Bee(num_dimensions) for _ in range(num_employed)]
        self.best_solution = min(self.employed_bees, key=lambda bee: bee.fitness)
        self.fitness_values = []
        self.best_fitness_values = []

    def run_algorithm(self):
        employed_bees_positions = []
        for iteration in range(self.max_iterations):
            # Фаза трудовых пчел
            self.employed_bees_phase()
            employed_bees_positions.append([bee.position for bee in self.employed_bees])

            # Вычисление вероятностей для фазы наблюдателей
            self.calculate_probs()

            # Фаза наблюдателей
            self.onlooker_bees_phase()

            # Фаза разведчиков
            self.scout_bees_phase()

            # Запись данных о фитнесе для визуализации
            self.fitness_values.append([bee.fitness for bee in self.employed_bees])
            self.best_fitness_values.append(
                (self.best_solution.position, self.best_solution.fitness)
            )

            # Вывод информации о лучшем решении на текущей итерации
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
        for bee in self.employed_bees:
            # Выбор случайной соседней пчелы и обновление позиции текущей пчелы
            neighbor_bee = random.choice(self.employed_bees)
            while neighbor_bee is bee:
                neighbor_bee = random.choice(self.employed_bees)
            new_position = [
                bee.position[i]
                + random.uniform(-1, 1) * (bee.position[i] - neighbor_bee.position[i])
                for i in range(self.num_dimensions)
            ]
            new_fitness = rastrigin_function(new_position)
            if new_fitness < bee.fitness:
                bee.update(new_position, new_fitness)

    def calculate_probs(self):
        # Вычисление вероятностей выбора пчел в фазе наблюдателей
        total_fitness = sum(bee.fitness for bee in self.employed_bees)
        self.probabilities = [bee.fitness / total_fitness for bee in self.employed_bees]

    def onlooker_bees_phase(self):
        for _ in range(self.num_onlookers):
            # Выбор трудовой пчелы на основе вероятностей и обновление её позиции
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
            new_fitness = rastrigin_function(new_position)
            if new_fitness < selected_bee.fitness:
                selected_bee.update(new_position, new_fitness)

    def scout_bees_phase(self):
        for bee in self.employed_bees:
            # Проверка, если найдена пчела с лучшим фитнесом, чем у текущего лучшего решения
            if bee.fitness > self.best_solution.fitness:
                self.best_solution = bee


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
    abc_algorithm = ABCAlgorithm(num_employed, num_onlookers, max_iterations)
    (
        best_solution,
        fitness_values,
        best_fitness_values,
        employed_bees_positions,
    ) = abc_algorithm.run_algorithm()

    logger.info(
        f"Best solution found at position {best_solution.position} with fitness {best_solution.fitness}"
    )

    iterations = list(range(max_iterations))
    # plot_fitness_progression_matplotlib(
    #     iterations, fitness_values, best_fitness_values, employed_bees_positions
    # )
