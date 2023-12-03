import numpy as np
import pandas as pd
import plotly.express as px
from numpy import ndarray
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from pr3_logistic_regression.model.logreg import LogisticRegression


def preprocess_data(df, test_size=0.25) -> tuple[ndarray, ndarray, ndarray, ndarray]:
    X = StandardScaler().fit_transform(df.drop("Outcome", axis=1))
    y = df["Outcome"]
    return train_test_split(X, y, test_size=test_size, random_state=0)


def train_and_evaluate(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Test Accuracy: {np.mean(y_pred == y_test) * 100:.2f}%\n")
    # print(f"classification_report\n{classification_report(y_test, y_pred)}")


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

    print("1. Train and evaluate sklearn logistic regression model\n")
    train_and_evaluate(linear_model.LogisticRegression(), *preprocess_data(df))

    print("2. Train and evaluate logistic regression model\n")
    train_and_evaluate(LogisticRegression(), *preprocess_data(df))

    print("3. Train and evaluate logistic regression model with selected features\n")
    drop_columns = [
        "BloodPressure",
        "SkinThickness",
        "Age",
    ]
    clean_df = df.drop(drop_columns, axis="columns")
    train_and_evaluate(LogisticRegression(), *preprocess_data(clean_df))
