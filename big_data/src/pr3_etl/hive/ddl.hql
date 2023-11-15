DROP TABLE products;
CREATE EXTERNAL TABLE IF NOT EXISTS products
(
    type          STRING,
    product_id    INT,
    product_name  STRING,
    product_price FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
LOCATION "/user/ivanovnp/warehouse/products"
TBLPROPERTIES ("skip.header.line.count" = "1");

DROP TABLE orders;
CREATE EXTERNAL TABLE IF NOT EXISTS orders
(
    type       STRING,
    order_id   INT,
    product_id INT,
    quantity   INT,
    order_date STRING,
    customer_id INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
LOCATION "/user/ivanovnp/warehouse/orders"
TBLPROPERTIES ("skip.header.line.count" = "1");

DROP TABLE customers;
CREATE EXTERNAL TABLE IF NOT EXISTS customers
(
    type           STRING,
    customer_id    INT,
    customer_name  STRING,
    customer_email STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
LOCATION "/user/ivanovnp/warehouse/customers"
TBLPROPERTIES ("skip.header.line.count" = "1");
