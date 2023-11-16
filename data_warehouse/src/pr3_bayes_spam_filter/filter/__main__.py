import json
import math
import pathlib
import re
from collections import defaultdict

import pandas as pd
from colorama import init, Fore, Style

init()


class NaiveBayesModel:
    def __init__(self):
        self.class_probabilities = defaultdict(float)
        self.word_probabilities = defaultdict(lambda: defaultdict(float))
        self.spam_words = set()

    def train(self, training_data):
        total_count = len(training_data)
        spam_count = sum(training_data["class"] == "spam")

        self.class_probabilities["spam"] = spam_count / total_count
        self.class_probabilities["ham"] = (total_count - spam_count) / total_count

        spam_words = defaultdict(int)
        ham_words = defaultdict(int)

        exclude_words = {
            "and",
            "the",
            "in",
            "to",
            "of",
            "a",
            "an",
            "is",
            "it",
            "on",
            "with",
            "for",
        }

        for _, entry in training_data.iterrows():
            _class, text = entry["class"], entry["text"]
            words = self.get_words(text)
            words = [w for w in words if w not in exclude_words]

            for word in words:
                if _class == "spam":
                    spam_words[word] += 1
                    self.spam_words.add(word)
                else:
                    ham_words[word] += 1

        for word in set(spam_words.keys()).union(set(ham_words.keys())):
            self.word_probabilities["spam"][word] = (spam_words[word] + 1) / (
                spam_count + 2
            )
            self.word_probabilities["ham"][word] = (ham_words[word] + 1) / (
                (total_count - spam_count) + 2
            )

        for _class in list(self.word_probabilities.keys()):
            _class_wp = list(self.word_probabilities[_class].items())[:50]
            _class_wp = tuple(map(lambda c: (c[0], round(c[1], 5)), _class_wp))
            print(
                f"word_probabilities - '{_class}': {json.dumps(dict(_class_wp), indent=2)}\n"
            )

    @staticmethod
    def get_words(text):
        return re.findall(r"\b\w+\b", text.lower())

    def predict(self, text):
        words = self.get_words(text)
        spam_score = math.log(self.class_probabilities["spam"])
        ham_score = math.log(self.class_probabilities["ham"])
        text_spam_words = set()

        for word in words:
            spam_score += math.log(self.word_probabilities["spam"].get(word, 1e-10))
            ham_score += math.log(self.word_probabilities["ham"].get(word, 1e-10))
            if spam_score > ham_score and word in self.spam_words:
                text_spam_words.add(word)

        spam_percentage = (
            round((len(text_spam_words) / len(words)) * 100, 2)
            if len(text_spam_words) > 0
            else None
        )

        return (
            "spam" if spam_score > ham_score else "ham",
            text_spam_words,
            spam_percentage,
        )


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
    df = pd.read_csv(
        pathlib.Path(__file__).parent.parent.joinpath("input/spamdb.csv"),
        encoding="utf-8",
        usecols=["class", "text"],
    )

    train_df, test_df = split_data(df, split_ratio=0.6)

    model = NaiveBayesModel()
    model.train(train_df)

    test_texts = test_df["text"].tolist()

    print("Prediction:\n")
    predictions = []
    for text in test_texts:
        result, spam_words, spam_percent = model.predict(text)
        words = model.get_words(text)
        if spam_words:
            words = [
                f"{Fore.RED}{w}{Style.RESET_ALL}" if w.lower() in spam_words else w
                for w in words
            ]
            text = " ".join(words)

        notif = (
            f" {Fore.RED}[{result.upper()}]{Style.RESET_ALL}"
            if result == "spam"
            else None
        )
        print(f"Message{notif or ''}:\n\t{Fore.LIGHTWHITE_EX}{text}{Style.RESET_ALL}")
        print(
            f"Spam percent: {f'{spam_percent}%' if spam_percent else ''}\n"
            f"Spam words: {spam_words if len(spam_words) > 0 else ''}\n"
        )
        predictions.append(result)

    true_labels = test_df["class"].tolist()
    accuracy = calculate_accuracy(predictions, true_labels)

    print(f"Accuracy: {accuracy * 100:.2f}%")
