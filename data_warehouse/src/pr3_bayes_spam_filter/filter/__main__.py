import math
import re
from collections import defaultdict

import pandas as pd


class NaiveBayesTrainer:
    def train(self, classifier, training_data):
        total_count = len(training_data)
        spam_count = sum(training_data["class"] == "spam")

        # Calculate class probabilities
        classifier.class_probabilities["spam"] = spam_count / total_count
        classifier.class_probabilities["ham"] = (total_count - spam_count) / total_count

        # Calculate word probabilities
        spam_words = defaultdict(int)
        ham_words = defaultdict(int)

        for index, entry in training_data.iterrows():
            label, text = entry["class"], entry["text"]
            words = re.findall(r"\b\w+\b", text.lower())

            for word in words:
                if label == "spam":
                    spam_words[word] += 1
                else:
                    ham_words[word] += 1

        for word in set(spam_words.keys()).union(set(ham_words.keys())):
            classifier.word_probabilities["spam"][word] = (spam_words[word] + 1) / (
                spam_count + 2
            )
            classifier.word_probabilities["ham"][word] = (ham_words[word] + 1) / (
                (total_count - spam_count) + 2
            )


class NaiveBayesClassifier:
    def __init__(self):
        self.class_probabilities = defaultdict(float)
        self.word_probabilities = defaultdict(lambda: defaultdict(float))

    def predict(self, text):
        words = re.findall(r"\b\w+\b", text.lower())
        spam_score = math.log(self.class_probabilities["spam"])
        ham_score = math.log(self.class_probabilities["ham"])

        for word in words:
            spam_score += math.log(self.word_probabilities["spam"].get(word, 1e-10))
            ham_score += math.log(self.word_probabilities["ham"].get(word, 1e-10))

        return "spam" if spam_score > ham_score else "ham"


def split_data(data, split_ratio=0.8):
    split_index = int(len(data) * split_ratio)
    training_data = data[:split_index]
    testing_data = data[split_index:]
    return training_data, testing_data


def calculate_accuracy(predictions, true_labels):
    correct_count = sum(
        1 for pred, true_label in zip(predictions, true_labels) if pred == true_label
    )
    total_count = len(true_labels)
    accuracy = correct_count / total_count
    return accuracy


if __name__ == "__main__":
    data = pd.read_csv(
        "../input/spamdb.csv", encoding="utf-8", usecols=["class", "text"]
    )

    training_data, testing_data = split_data(data)

    classifier = NaiveBayesClassifier()

    trainer = NaiveBayesTrainer()
    trainer.train(classifier, training_data)

    test_texts = testing_data["text"].tolist()
    true_labels = testing_data["class"].tolist()

    predictions = [classifier.predict(text) for text in test_texts]
    accuracy = calculate_accuracy(predictions, true_labels)

    print(f"Accuracy: {accuracy * 100:.2f}%")
