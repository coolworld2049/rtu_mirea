from mrjob.job import MRJob


class StripesAlgorithm(MRJob):
    def mapper(self, _, line):
        # Parse the input line into a list of products
        products = line.strip().split(",")

        # Emit stripes for each product with its associated products
        for product in products:
            yield product, {p: 1 for p in products if p != product}

    def reducer(self, key, values):
        # Merge the final stripe dictionaries
        combined_stripe = {}
        for stripe in values:
            for product, count in stripe.items():
                combined_stripe[product] = combined_stripe.get(product, 0) + count

        yield key, combined_stripe


if __name__ == "__main__":
    StripesAlgorithm.run()
