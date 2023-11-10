from mrjob.job import MRJob


class OrderCountMRJob(MRJob):
    def mapper(self, _, line):
        fields = line.split(",")
        product_name = fields[2]
        yield product_name, 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == "__main__":
    OrderCountMRJob.run()
