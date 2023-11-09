import argparse
import pathlib
import random

from loguru import logger
from mimesis import Generic


def gen_db(
    output_path: pathlib.Path,
    product_number: int,
    rand_range: list[int],
    delimiter: str,
):
    generic = Generic()
    fake_products = [generic.text.word().replace(" ", "") for _ in range(100)]
    product_names = ""
    for a in range(product_number):
        _product_names = delimiter.join(
            set(
                random.choices(
                    fake_products, k=random.randint(rand_range[0], rand_range[1])
                )
            )
        )
        if a != product_number - 1:
            _product_names += "\n"
        product_names += _product_names
    output_path.write_text(product_names)
    logger.debug(f"Created {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_path")
    parser.add_argument("-n", "--product_number", default=200, type=int)
    parser.add_argument("-rr", "--rand_range", default="2,10", help="start,stop")
    parser.add_argument("-d", "--delimiter", default=",")
    args = parser.parse_args()
    gen_db(
        output_path=pathlib.Path(__file__).parent.joinpath(args.output_path),
        product_number=args.product_number,
        rand_range=[int(x) for x in args.rand_range.split(",")],
        delimiter=args.delimiter,
    )
