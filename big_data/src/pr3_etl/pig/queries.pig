products = LOAD 'warehouse/products/products.csv' USING PigStorage(',') AS (
    type: chararray,
    product_id: int,
    product_name: chararray,
    product_price: int
);

orders = LOAD 'warehouse/orders/orders.csv' USING PigStorage(',') AS (
    type: chararray,
    order_id: int,
    product_id: int,
    quantity: int,
    order_date: chararray,
    customer_id: int
);

customers = LOAD 'warehouse/customers/customers.csv' USING PigStorage(',') AS (
    type: chararray,
    customer_id: int,
    customer_name: chararray,
    customer_email: chararray
);

-- 1
filtered_customers = FILTER customers BY customer_name MATCHES '.*Johnson.*';
result_1 = FOREACH filtered_customers GENERATE *;
STORE result_1 INTO 'warehouse/pig/output/q1' USING PigStorage(',');

-- 2
filtered_customers_q2 = FILTER customers BY customer_name MATCHES 'J.*';
result_2 = FOREACH filtered_customers_q2 GENERATE *;
STORE result_2 INTO 'warehouse/pig/output/q2' USING PigStorage(',');

-- 3
filtered_orders = FILTER orders BY order_date > '2023-10-18';
STORE filtered_orders INTO 'warehouse/pig/output/q3' USING PigStorage(',');

-- 4
expensive_products = FILTER products BY product_price > 150;
STORE expensive_products INTO 'warehouse/pig/output/q4' USING PigStorage(',');

-- 5
joined_data = JOIN orders BY product_id, products BY product_id;
grouped_data = GROUP joined_data BY (products::product_name, products::product_price);
result_5 = FOREACH grouped_data GENERATE
    group.products::product_name AS product_name,
    group.products::product_price AS product_price,
    SUM(joined_data.quantity) AS total_quantity;
STORE result_5 INTO 'warehouse/pig/output/q5' USING PigStorage(',');
