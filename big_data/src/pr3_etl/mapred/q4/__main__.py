from mrjob.job import MRJob


class Query4Job(MRJob):
    def mapper(self, _, line):
        fields = line.strip().split(",")
        if fields[0] == "customer":
            (
                record_type,
                customer_id,
                customer_name,
                customer_email,
            ) = fields
            yield customer_id, 1

    def combiner(self, customer_id, counts):
        yield customer_id, sum(counts)

    def reducer(self, customer_id, counts):
        total_orders = sum(counts)
        yield customer_id, total_orders


if __name__ == "__main__":
    Query4Job.run()
