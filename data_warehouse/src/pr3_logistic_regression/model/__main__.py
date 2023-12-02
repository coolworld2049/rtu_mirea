import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class LogisticRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.theta = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        X = np.c_[np.ones((X.shape[0], 1)), X]
        self.theta = np.zeros(X.shape[1])

        for _ in range(self.iterations):
            h = self.sigmoid(X @ self.theta)
            gradient = X.T @ (h - y) / len(y)
            self.theta -= self.learning_rate * gradient

    def predict(self, X, threshold=0.5):
        X = np.c_[np.ones((X.shape[0], 1)), X]
        return (self.sigmoid(X @ self.theta) >= threshold).astype(int)


def select_features(data):
    correlation_matrix = data.corr()
    return (
        correlation_matrix["Outcome"]
        .abs()
        .sort_values(ascending=False)[1:3]
        .index.tolist()
    )


def preprocess_data(data):
    X = StandardScaler().fit_transform(data.drop("Outcome", axis=1))
    return train_test_split(X, data["Outcome"], test_size=0.2, random_state=42)


def train_and_evaluate(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    accuracy = np.mean(model.predict(X_test) == y_test)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")


if __name__ == "__main__":
    file_path = "../input/diabetes.csv"
    data = pd.read_csv(file_path)

    # Train and evaluate logistic regression model
    X_train, X_test, y_train, y_test = preprocess_data(data)
    logistic_model = LogisticRegression()
    train_and_evaluate(logistic_model, X_train, X_test, y_train, y_test)

    # Train and evaluate logistic regression model with selected features
    selected_features = select_features(data)
    X_new, _, y_new, _ = preprocess_data(data[selected_features + ["Outcome"]])
    logistic_model_new = LogisticRegression()
    train_and_evaluate(logistic_model_new, X_new, X_new, y_new, y_new)
