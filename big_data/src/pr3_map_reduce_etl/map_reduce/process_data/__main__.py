from datetime import datetime

from mrjob.job import MRJob
from mrjob.protocol import TextProtocol
from mrjob.step import MRStep


class ProcessData(MRJob):
    OUTPUT_PROTOCOL = TextProtocol

    def configure_args(self):
        super(ProcessData, self).configure_args()
        self.add_file_arg("--products")
        self.add_file_arg("--orders")
        self.add_file_arg("--customers")

    @staticmethod
    def load_products(_, line):
        product_id, product_name, product_price = map(str.strip, line.split(","))
        yield int(product_id), (product_name, int(product_price))

    @staticmethod
    def load_orders(_, line):
        order_id, user_id, product_id, quantity, order_date, customer_id = map(
            str.strip, line.split(",")
        )
        yield int(product_id), (int(quantity), order_date)

    @staticmethod
    def load_customers(_, line):
        customer_id, customer_name, customer_email, product_id, order_date = map(
            str.strip, line.split(",")
        )
        yield int(product_id), (customer_name, customer_email, order_date)

    def steps(self):
        return [
            MRStep(mapper=self.load_products),
            MRStep(mapper=self.load_orders),
            MRStep(mapper=self.load_customers),
            MRStep(reducer=self.filter_products),
            MRStep(reducer=self.filter_orders),
            MRStep(reducer=self.extract_customer_names),
            MRStep(reducer=self.filter_customers),
            MRStep(reducer=self.join_and_aggregate),
            MRStep(reducer=self.join_and_project),
            MRStep(reducer=self.join_and_filter),
        ]

    @staticmethod
    def filter_products(product_id, values):
        for product_name, product_price in values:
            if product_price > 200:
                yield product_id, (product_name, product_price)

    @staticmethod
    def filter_orders(product_id, values):
        for quantity, order_date in values:
            order_date = datetime.strptime(order_date, "%Y-%m-%d")
            if order_date > datetime.strptime("2023-10-18", "%Y-%m-%d"):
                yield product_id, (quantity, order_date)

    @staticmethod
    def extract_customer_names(product_id, values):
        for customer_name, _, _ in values:
            yield product_id, customer_name

    @staticmethod
    def filter_customers(product_id, values):
        for customer_name, customer_email, _ in values:
            if customer_name.startswith("J"):
                yield product_id, (customer_name, customer_email)

    @staticmethod
    def join_and_aggregate(product_id, values):  # noqa
        joined_data = list(values)
        if len(joined_data) == 2:  # Ensure both tables have data for the product
            orders_data, products_data = joined_data
            product_name, product_price = products_data[0], products_data[1]
            total_quantity = sum(orders[0] for orders in orders_data)
            yield None, (product_name, product_price, total_quantity)

    @staticmethod
    def join_and_project(product_id, values):  # noqa
        joined_data = list(values)
        if len(joined_data) == 2:  # Ensure both tables have data for the product
            customers_data, products_data = joined_data
            customer_name, customer_email, _, _ = customers_data[0]
            product_name, product_price = products_data[0], products_data[1]
            yield None, (customer_name, customer_email, product_name, product_price)

    @staticmethod
    def join_and_filter(product_id, values):  # noqa
        joined_data = list(values)
        if len(joined_data) == 2:  # Ensure both tables have data for the product
            customers_data, orders_data = joined_data
            customer_name, customer_email, _, _ = customers_data[0]
            yield None, (customer_name, customer_email)


if __name__ == "__main__":
    ProcessData.run()
