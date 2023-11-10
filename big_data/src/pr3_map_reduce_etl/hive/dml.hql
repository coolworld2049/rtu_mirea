LOAD DATA INPATH '/opt/hive/data/products.csv'
OVERWRITE INTO TABLE products;

LOAD DATA INPATH '/opt/hive/data/orders.csv'
OVERWRITE INTO TABLE orders;

LOAD DATA INPATH '/opt/hive/data/customers.csv'
OVERWRITE INTO TABLE customers;
