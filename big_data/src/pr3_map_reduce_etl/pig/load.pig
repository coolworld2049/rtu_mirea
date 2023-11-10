customers = LOAD '/path/to/customers_data.csv' USING PigStorage(',') AS (customer_id:int, customer_name:chararray, email:chararray, address:chararray);
orders = LOAD '/path/to/orders_data.csv' USING PigStorage(',') AS (order_id:int, customer_id:int, order_date:chararray, total_amount:double);
products = LOAD '/path/to/products_data.csv' USING PigStorage(',') AS (product_id:int, product_name:chararray, price:double);
