CREATE TABLE customer
(
    customer_id   INT,
    customer_name STRING,
    email         STRING,
    address       STRING
);

CREATE TABLE orders
(
    order_id     INT,
    customer_id  INT,
    order_date   STRING,
    total_amount DOUBLE
);

CREATE TABLE products
(
    product_id   INT,
    product_name STRING,
    price        DOUBLE
);