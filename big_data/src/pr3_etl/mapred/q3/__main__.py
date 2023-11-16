from datetime import datetime
from mrjob.job import MRJob


class Query3Job(MRJob):
    def mapper(self, _, line):
        record_type, *fields = line.strip().split(",")
        if record_type == "order":
            if datetime.strptime(fields[3], "%Y-%m-%d") > datetime.strptime(
                "2023-10-18", "%Y-%m-%d"
            ):
                yield None, line


if __name__ == "__main__":
    Query3Job.run()
