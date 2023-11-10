products = LOAD '/opt/hive/data/products.csv' USING PigStorage(',') AS (
    product_id: int,
    product_name: chararray,
    product_price: int
);

orders = LOAD '/opt/hive/data/orders.csv' USING PigStorage(',') AS (
    order_id: int,
    user_id: int,
    product_id: int,
    quantity: int,
    order_date: chararray,
    customer_id: int
);

customers = LOAD '/opt/hive/data/customers.csv' USING PigStorage(',') AS (
    customer_id: int,
    customer_name: chararray,
    customer_email: chararray,
    product_id: int,
    order_date: chararray
);

-- 1
filtered_products = FILTER products BY product_price > 200;
STORE filtered_products INTO 'output_filtered_products' USING PigStorage(',');

-- 2
filtered_orders = FILTER orders BY ToDate(order_date, 'yyyy-MM-dd') > ToDate('2023-10-18', 'yyyy-MM-dd');
STORE filtered_orders INTO 'output_filtered_orders' USING PigStorage(',');

-- 3
customer_names = FOREACH customers GENERATE customer_name;
STORE customer_names INTO 'output_customer_names' USING PigStorage(',');

-- 4
filtered_customers = FILTER customers BY SUBSTRING(customer_name, 0, 1) == 'J';
STORE filtered_customers INTO 'output_filtered_customers' USING PigStorage(',');

-- 5
joined_data = JOIN orders BY product_id, products BY product_id;
aggregated_data = FOREACH (GROUP joined_data BY (products::product_name, products::product_price))
    GENERATE group.product_name AS product_name, group.product_price AS product_price, SUM(joined_data.quantity) AS total_quantity;
STORE aggregated_data INTO 'output_aggregated_data' USING PigStorage(',');

-- 6
joined_tables = JOIN customers BY product_id, products BY product_id;
result = FOREACH joined_tables
    GENERATE customers::customer_name AS customer_name,
    customers::customer_email AS customer_email,
    products::product_name AS product_name,
    products::product_price AS product_price;
STORE result INTO 'output_joined_tables' USING PigStorage(',');

-- 7
joined_tables_filtered = JOIN customers BY (product_id, order_date), orders BY (product_id, order_date);
STORE joined_tables_filtered INTO 'output_joined_tables_filtered' USING PigStorage(',');
