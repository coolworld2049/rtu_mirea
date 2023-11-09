from mrjob.job import MRJob


class CrossCorrelationPairs(MRJob):
    def mapper(self, _, line):
        items = line.strip().split(",")
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                yield (items[i], items[j]), 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == "__main__":
    CrossCorrelationPairs.run()
