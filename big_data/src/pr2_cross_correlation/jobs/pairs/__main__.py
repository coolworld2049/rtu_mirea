from mrjob.job import MRJob
from mrjob.step import MRStep


class CrossCorrelationPairs(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]

    def mapper(self, _, line):
        items = line.strip().split(",")

        # Формирует все возможные пары товаров в строке и передает их в reducer
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                yield (items[i], items[j]), 1

    def reducer(self, key, values):
        # Суммирует значения для каждой уникальной пары товаров
        yield key, sum(values)


if __name__ == "__main__":
    CrossCorrelationPairs.run()
