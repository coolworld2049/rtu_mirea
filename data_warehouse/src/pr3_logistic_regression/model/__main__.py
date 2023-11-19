import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class DataNormalizer:
    @staticmethod
    def normalize_data(X_train, X_test):
        scaler = StandardScaler()
        X_train_normalized = scaler.fit_transform(X_train)
        X_test_normalized = scaler.transform(X_test)
        return X_train_normalized, X_test_normalized


class LogisticRegression:
    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def cost_function(X, y, theta):
        m = len(y)
        h = LogisticRegression.sigmoid(X.dot(theta))
        cost = (1 / m) * (-y.dot(np.log(h)) - (1 - y).dot(np.log(1 - h)))
        return cost

    @staticmethod
    def gradient_descent(X, y, theta, learning_rate, iterations):
        m = len(y)
        cost_history = np.zeros(iterations)

        for i in range(iterations):
            gradient = X.T.dot(LogisticRegression.sigmoid(X.dot(theta)) - y) / m
            theta = theta - learning_rate * gradient
            cost_history[i] = LogisticRegression.cost_function(X, y, theta)

        return theta, cost_history

    @staticmethod
    def predict(X, theta):
        return LogisticRegression.sigmoid(X.dot(theta))

    @staticmethod
    def accuracy(y_true, y_pred):
        y_pred_class = (y_pred >= 0.5).astype(int)
        return np.mean(y_true == y_pred_class)


class FeatureSelector:
    @staticmethod
    def select_features(data, threshold=0.8):
        correlation_matrix = data.corr().abs()
        upper_triangle: DataFrame = correlation_matrix.where(
            np.triu(np.ones(correlation_matrix.shape), k=1).astype(np.bool_)
        )
        to_drop = {
            i: column
            for i, column in enumerate(upper_triangle.columns)
            if any(upper_triangle[column] > threshold)
        }
        return to_drop


if __name__ == "__main__":
    file_path = "../input/diabetes.csv"
    data = pd.read_csv(file_path)

    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=42
    )

    data_normalizer = DataNormalizer()
    X_train_normalized, X_test_normalized = data_normalizer.normalize_data(
        X_train, X_test
    )

    logistic_regression = LogisticRegression()
    X_train_normalized = np.c_[
        np.ones((X_train_normalized.shape[0], 1)), X_train_normalized
    ]
    theta, cost_history = logistic_regression.gradient_descent(
        X_train_normalized, y_train, np.zeros(X_train_normalized.shape[1]), 0.01, 1000
    )

    feature_selector = FeatureSelector()
    to_drop = feature_selector.select_features(data, threshold=0.4)

    X_train_selected = np.delete(X_train_normalized, list(to_drop.keys()), axis=1)
    X_test_selected = np.delete(X_test_normalized, list(to_drop.keys()), axis=1)

    theta_selected, _ = logistic_regression.gradient_descent(
        X_train_selected, y_train, np.zeros(X_train_selected.shape[1]), 0.01, 1000
    )

    y_train_pred = logistic_regression.predict(X_train_selected, theta_selected)
    y_test_pred = logistic_regression.predict(
        np.c_[np.ones((X_test_selected.shape[0], 1)), X_test_selected], theta_selected
    )

    accuracy_train = logistic_regression.accuracy(y_train, y_train_pred)
    accuracy_test = logistic_regression.accuracy(y_test, y_test_pred)

    print(f"Точность на обучающей выборке: {accuracy_train}")
    print(f"Точность на тестовой выборке: {accuracy_test}")
