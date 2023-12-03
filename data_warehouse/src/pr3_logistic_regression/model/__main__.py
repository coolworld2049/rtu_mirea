import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import plotly.express as px


class LogisticRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.theta = None

    @staticmethod
    def sigmoid(z):
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


def preprocess_data(df):
    X = StandardScaler().fit_transform(df.drop("Outcome", axis=1))
    return train_test_split(X, df["Outcome"], test_size=0.2, random_state=42)


def train_and_evaluate(model: LogisticRegression, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Test Accuracy: {np.mean(y_test == y_pred) * 100:.2f}%\n")
    print(f"classification_report\n")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    df = pd.read_csv("../input/diabetes.csv")

    correlation_matrix = df.corr()
    fig = px.imshow(
        correlation_matrix,
        labels=dict(x="Features", y="Features", color="Correlation"),
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        color_continuous_scale="Viridis",
    )
    fig.update_layout(title="Correlation Matrix Heatmap", width=800, height=600)
    # fig.show()

    print("Train and evaluate logistic regression model\n")
    train_and_evaluate(LogisticRegression(), *preprocess_data(df))

    print("Train and evaluate logistic regression model with selected features\n")
    drop_columns = ["BloodPressure", "SkinThickness", "BMI", "Insulin"]
    clean_df = df.drop(drop_columns, axis="columns")
    train_and_evaluate(LogisticRegression(), *preprocess_data(clean_df))
