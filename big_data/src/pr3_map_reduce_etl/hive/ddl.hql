CREATE EXTERNAL TABLE IF NOT EXISTS products
(
    product_id    INT,
    product_name  STRING,
    product_price FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
TBLPROPERTIES ("skip.header.line.count" = "1");


CREATE EXTERNAL TABLE IF NOT EXISTS orders
(
    order_id   INT,
    user_id    INT,
    product_id INT,
    quantity   INT,
    order_date STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
TBLPROPERTIES ("skip.header.line.count" = "1");


CREATE EXTERNAL TABLE IF NOT EXISTS customers
(
    customer_id    INT,
    customer_name  STRING,
    customer_email STRING,
    product_id     INT,
    order_date     STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
TBLPROPERTIES ("skip.header.line.count" = "1");
