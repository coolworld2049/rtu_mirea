import pathlib

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import seaborn as sns

data = pd.read_csv(pathlib.Path(__file__).parent.parent.joinpath("input/diabetes.csv"))

sns.heatmap(data.corr(method="spearman"), annot=True)

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Шаг 1: Разбиение выборки на обучающую и тестовую
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# Шаг 2: Реализация логистической регрессии с использованием градиентного спуска
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def gradient_descent(X, y, theta, learning_rate, iterations):
    m = len(y)

    for _ in range(iterations):
        h = sigmoid(np.dot(X, theta))
        gradient = np.dot(X.T, (h - y)) / m
        theta -= learning_rate * gradient

    return theta


# Добавим столбец единиц к матрице признаков для учета свободного члена
X_train = np.c_[np.ones((X_train.shape[0], 1)), X_train]
X_test = np.c_[np.ones((X_test.shape[0], 1)), X_test]

# Инициализация параметров и обучение модели
theta = np.zeros(X_train.shape[1])
learning_rate = 0.01
iterations = 1000

theta = gradient_descent(X_train, y_train, theta, learning_rate, iterations)

# Шаг 3: Предсказание на тестовой выборке
predictions = sigmoid(np.dot(X_test, theta))
predicted_labels = (predictions >= 0.5).astype(int)

# Вычисление точности классификации
accuracy = accuracy_score(y_test, predicted_labels)
print(f"Точность классификации: {accuracy * 100:.2f}%")

# Шаг 4: Применение отбора признаков на основе корреляции
# Выберем 5 наилучших признаков
best_features = SelectKBest(score_func=chi2, k=5)
X_new = best_features.fit_transform(X, y)

# Разбиение нового признакового пространства
X_train_new, X_test_new, _, _ = train_test_split(
    X_new, y, test_size=0.2, random_state=42
)

# Инициализация и обучение новой модели на выбранных признаках
model_new = LogisticRegression()
model_new.fit(X_train_new, y_train)

# Предсказание на тестовой выборке
predicted_labels_new = model_new.predict(X_test_new)

# Вычисление точности новой модели
accuracy_new = accuracy_score(y_test, predicted_labels_new)
print(f"Точность классификации с отбором признаков: {accuracy_new * 100:.2f}%")
