from mrjob.job import MRJob


class Query5Job(MRJob):
    def mapper(self, _, line):
        record_type, *fields = line.strip().split(",")

        if record_type == "order":
            yield fields[2], (float(fields[3]), 1)

        elif record_type == "product":
            yield fields[0], ("product", float(fields[3]))

    def reducer(self, key, values):
        product_name = None
        product_price = None
        total_quantity = 0

        for value in values:
            record_type, data = value
            if record_type == "product":
                product_price = data
            elif record_type == "order":
                total_quantity += data[0]

        if product_price is not None:
            yield product_name, (product_name, product_price, total_quantity)


if __name__ == "__main__":
    Query5Job.run()
