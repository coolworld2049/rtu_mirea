import re

import pandas as pd
from collections import defaultdict

from pandas import Series
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

data = pd.read_csv("../input/spamdb.csv")
X = data["text"]
y = data["class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


class NaiveBayesClassifier:
    def __init__(self):
        self.class_probs = defaultdict(float)
        self.word_probs = defaultdict(lambda: defaultdict(float))

    @staticmethod
    def get_words(text):
        return re.findall(r"\b\w+\b", text.lower())

    def fit(self, X, y):
        total_messages = len(X)
        spam_messages = X[y == "spam"]
        ham_messages = X[y == "ham"]

        # Оценка вероятности классов
        self.class_probs["spam"] = len(spam_messages) / total_messages
        self.class_probs["ham"] = len(ham_messages) / total_messages

        # Оценка вероятности слов в каждом классе
        for message, label in zip(X, y):
            words = message.split()
            for word in words:
                self.word_probs[word][label] += 1

        # Нормализация вероятностей
        for word, class_counts in self.word_probs.items():
            total_word_count = sum(class_counts.values())
            for class_label, count in class_counts.items():
                self.word_probs[word][class_label] = count / total_word_count

    def predict(self, X):
        predictions = []
        for message in X:
            words = message.split()
            spam_prob = 1.0
            ham_prob = 1.0
            for word in words:
                spam_prob *= self.word_probs[word]["spam"]
                ham_prob *= self.word_probs[word]["ham"]

            spam_prob *= self.class_probs["spam"]
            ham_prob *= self.class_probs["ham"]

            if spam_prob > ham_prob:
                predictions.append("spam")
            else:
                predictions.append("ham")

        return predictions


# Использование наивного Байесовского классификатора
classifier = NaiveBayesClassifier()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

for i, item in enumerate(list(X_test.items())):
    print(f"{i}. Message: {item[1]}\nPredict: {classifier.predict([item[1]])[0]}\n")

# Оценка качества модели
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print(f"Confusion Matrix:\n{conf_matrix}")
print(f"Classification Report:\n{classification_rep}")
