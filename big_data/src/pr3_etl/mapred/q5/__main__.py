from mrjob.job import MRJob


class ProductTotalsJoinMRJob(MRJob):
    def mapper(self, _, line):
        fields = line.strip().split(",")

        record_type = fields[0]

        if record_type == "product":
            # (product_id, ('product', product_price))
            yield fields[1], ("product", [fields[2], fields[3]])
        elif record_type == "order":
            # (product_id, ('order', quantity))
            yield fields[2], ("order", fields[3])

    def reducer(self, key, values):
        product_info = None
        total_quantity = 0

        for record_type, value in values:
            if record_type == "product":
                product_info = value
            elif record_type == "order":
                total_quantity += float(value)

        if product_info is not None and total_quantity != 0:
            product_name, product_price = product_info
            yield product_name, (product_price, round(total_quantity, 1))


if __name__ == "__main__":
    ProductTotalsJoinMRJob.run()
