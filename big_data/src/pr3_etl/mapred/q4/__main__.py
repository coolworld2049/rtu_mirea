from mrjob.job import MRJob


class Query4Job(MRJob):
    def mapper(self, _, line):
        record_type, *fields = line.strip().split(",")
        if record_type == "product" and int(fields[3]) > 150:
            yield None, line


if __name__ == "__main__":
    Query4Job.run()
