from datetime import datetime

from mrjob.job import MRJob


class Query3Job(MRJob):
    def mapper(self, _, line):
        fields = line.strip().split(",")
        if fields[0] == "orders":
            (
                record_type,
                order_id,
                product_id,
                quantity,
                order_date,
                customer_id,
            ) = fields
            lt_datetime = datetime.strptime("2023-10-18", "%Y-%m-%d")
            if datetime.strptime(order_date, "%Y-%m-%d") > lt_datetime:
                yield fields[0], line


if __name__ == "__main__":
    Query3Job.run()
