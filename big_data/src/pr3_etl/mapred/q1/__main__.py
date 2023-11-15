from mrjob.job import MRJob


class Query1Job(MRJob):
    def mapper(self, _, line):
        fields = line.strip().split(",")
        if fields[0] == "customer":
            (
                record_type,
                customer_id,
                customer_name,
                customer_email,
            ) = fields
            if "Johnson" in customer_name:
                yield fields[0], line


if __name__ == "__main__":
    Query1Job.run()
