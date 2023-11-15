from mrjob.job import MRJob


class Query1Job(MRJob):
    def mapper(self, _, line):
        record_type, *fields = line.strip().split(",")
        if record_type == "customer" and "Johnson" in fields[1]:
            yield None, line


if __name__ == "__main__":
    Query1Job.run()
