from datetime import datetime

from mrjob.job import MRJob
from mrjob.step import MRStep


class Query1(MRJob):
    def configure_args(self):
        super(Query1, self).configure_args()
        self.add_file_arg("--customers", required=False)
        self.add_file_arg("--orders", required=False)
        self.add_file_arg("--products")

    def mapper(self, _, line):
        product_id, product_name, product_price = map(str, line.strip().split(","))
        if int(product_price) > 200:
            yield product_id, line

    def reducer(self, product_id, values):
        for value in values:
            yield product_id, value


class Query2(MRJob):
    def mapper(self, _, line):
        order_id, user_id, product_id, quantity, order_date, customer_id = map(
            str, line.strip().split(",")
        )
        try:
            order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
            if order_date is not None:
                yield order_id, line
        except ValueError:
            pass

    def reducer(self, order_id, values):
        for value in values:
            yield order_id, value


class Query3(MRJob):
    def mapper(self, _, line):
        customer_name = line.strip()
        yield customer_name, None

    def reducer(self, customer_name, _):
        yield None, customer_name


class Query4(MRJob):
    def mapper(self, _, line):
        customer_id, customer_name, customer_email, product_id, order_date = map(
            str, line.strip().split(",")
        )
        if customer_name.startswith("J"):
            yield customer_id, line

    def reducer(self, customer_id, values):
        for value in values:
            yield customer_id, value


class Query5(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_join, reducer=self.reducer_join),
            MRStep(reducer=self.reducer_aggregate),
        ]

    def mapper_join(self, _, line):
        # Assuming the line format is 'id, name, price' for both products and orders
        data = line.strip().split(",")
        record_type = data[0]  # 'p' for products, 'o' for orders

        if record_type == "product":
            product_id, product_name, product_price = data[1:]
            yield product_id, ("product", product_name, int(product_price))
        elif record_type == "o":
            order_id, _, product_id, quantity, _, _ = data[1:]
            yield product_id, ("order", int(quantity))

    def reducer_join(self, product_id, values):
        product_info = None
        order_quantities = []

        for value in values:
            record_type, *info = value

            if record_type == "product":
                product_info = info
            elif record_type == "order":
                order_quantities.append(info[0])

        if product_info is not None:
            for quantity in order_quantities:
                yield product_info, quantity

    def reducer_aggregate(self, product_info, quantities):
        total_quantity = sum(quantities)
        yield product_info, total_quantity


if __name__ == "__main__":
    Query1.run()