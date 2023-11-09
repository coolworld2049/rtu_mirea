from mrjob.job import MRJob


class CrossCorrelationStripes(MRJob):
    def mapper(self, _, line):
        items = line.strip().split(",")
        for i in range(len(items)):
            stripe = {}
            for j in range(len(items)):
                if i != j:
                    if items[j] not in stripe:
                        stripe[items[j]] = 1
                    else:
                        stripe[items[j]] += 1
            yield items[i], stripe

    def reducer(self, key, values):
        result = {}
        for value in values:
            for k, v in value.items():
                if k not in result:
                    result[k] = v
                else:
                    result[k] += v
        yield key, result


if __name__ == "__main__":
    CrossCorrelationStripes.run()
