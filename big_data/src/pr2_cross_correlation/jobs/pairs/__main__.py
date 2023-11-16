from mrjob.job import MRJob


class PairsAlgorithm(MRJob):
    def mapper(self, _, line):
        # Parse the input line into a list of products
        products = line.strip().split(",")

        # Emit pairs for each product combination
        for i in range(len(products)):
            for j in range(i + 1, len(products)):
                yield tuple(sorted([products[i], products[j]])), 1

    def reducer(self, key, values):
        # Output the pair count for pairs
        yield key, sum(values)


if __name__ == "__main__":
    PairsAlgorithm.run()
