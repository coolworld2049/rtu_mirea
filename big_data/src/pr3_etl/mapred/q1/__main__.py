from mrjob.job import MRJob
from mrjob.step import MRStep


class Query1Job(MRJob):
    def mapper(self, _, line):
        record_type, *fields = line.strip().split(",")
        if record_type == "customer" and "Johnson" in fields[1]:
            yield None, line

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
            )
        ]


if __name__ == "__main__":
    Query1Job.run()
