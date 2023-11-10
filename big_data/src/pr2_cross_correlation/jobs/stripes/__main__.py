from mrjob.job import MRJob
from mrjob.step import MRStep


class CrossCorrelationStripes(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper, combiner=self.combiner, reducer=self.reducer)
        ]

    def mapper(self, _, line):
        items = line.strip().split(",")

        # Формирует словарь для каждого товара, где ключ - другие товары, значение - количество вхождений
        for i in range(len(items)):
            stripe = {item: 1 for item in items if item != items[i]}
            yield items[i], stripe

    def combiner(self, key, values):
        # Комбинирует данные на mapper, суммируя словари для каждого товара
        combined_stripe = {}
        for stripe in values:
            for item, count in stripe.items():
                combined_stripe[item] = combined_stripe.get(item, 0) + count
        yield key, combined_stripe

    def reducer(self, key, values):
        # Суммирует словари для каждого товара
        combined_stripe = {}
        for stripe in values:
            for item, count in stripe.items():
                combined_stripe[item] = combined_stripe.get(item, 0) + count
        yield key, combined_stripe


if __name__ == "__main__":
    CrossCorrelationStripes.run()
