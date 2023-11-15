from mrjob.job import MRJob


class Query5Job(MRJob):
    def mapper(self, _, line):
        fields = line.strip().split(",")
        if fields[0] == "order":
            record_type, _, product_id, quantity, _, _ = fields
            yield product_id, float(quantity)

    def reducer(self, product_id, values):
        yield product_id, sum(values)


if __name__ == "__main__":
    Query5Job.run()
