import numpy as np
from numpy import ndarray


class LogisticRegression:
    def __init__(self, learning_rate=1e-1, convergence_threshold=1e-2, verbose=0):
        self.alpha = learning_rate
        self.convergence_threshold = convergence_threshold
        self.theta: ndarray | None = None
        self.verbose = verbose

    @staticmethod
    def _sigmoid(z):
        return 1 / (1 + np.exp(-z))

    def _gradient(self, X, y):
        """
        ∇J(theta) = (1/m) * X^T * (sigmoid(theta^T X) - y)
        :param X:
        :param y:
        :return:
        """
        m = len(y)
        # h_theta(X) = sigmoid(theta^T X)
        hypothesis = self._sigmoid(np.dot(X, self.theta))
        # ∇J(theta) = (1/m) * X^T   * (h_theta(X) - y)
        gradient = np.dot(X.transpose(), (hypothesis - y)) / m
        return gradient

    def fit(self, X, y):
        """
        Алгоритм сошелся когда изменения весов становятся достаточно маленькими,
        и модель приблизительно соответствует оптимальным значениям параметров.
        :param X:
        :param y:
        :return:
        """
        X: ndarray = np.c_[np.ones((X.shape[0], 1)), X]
        self.theta = np.zeros(X.shape[1])
        last_theta = np.copy(self.theta)
        iteration = 0
        while True:
            gradient = self._gradient(X, y)
            self.theta -= self.alpha * gradient
            euclidean_norm = np.linalg.norm(self.theta - last_theta)
            if self.verbose == 1:
                print(
                    f"iteration: {iteration}\ntheta: {self.theta}\neuclidean_norm: {euclidean_norm}\n"
                )
            if euclidean_norm < self.convergence_threshold:
                print(f"Iterations {iteration}\n")
                print(f"Euclidean norm is {euclidean_norm}\n")
                break
            last_theta = np.copy(self.theta)
            iteration += 1

    def predict(self, X, threshold=0.5):
        """
        Для предсказания просто подставляем обученные веса в гипотезу и применяем пороговое значение.

        :param X:
        :param threshold:
        :return:
        """
        X = np.c_[np.ones((X.shape[0], 1)), X]
        probabilities = self._sigmoid(np.dot(X, self.theta))
        predictions = (probabilities > threshold).astype(int)
        return predictions
