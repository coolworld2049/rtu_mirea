import hdfs
from pyhive import hive


# устанавливаем соединение с Hive
conn = hive.Connection(
    host="localhost", port=10000, username="sasha", database="default"
)
cursor = conn.cursor()

# создаем таблицу products
create_table_query = """
CREATE TABLE products (
    product_id INT,
    product_name STRING,
    product_price FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
"""

cursor.execute(create_table_query)

# загружаем данные из файла в таблицу products
load_data_query = """
LOAD DATA INPATH '/user/sasha/warehouse/products.csv'
OVERWRITE INTO TABLE products
"""
cursor.execute(load_data_query)


# функция для сохранения результатов запроса в HDFS-каталоге
def save_results(output_directory, query, result_num):
    save_query = f"""
    INSERT OVERWRITE DIRECTORY '{output_directory}/result_{result_num}'
    {query}
    """
    cursor.execute(save_query)


# выбираем все записи из таблицы products
select_query = """
SELECT * FROM products
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 1)

# выбираем товары с ценой больше 200
select_query = """
SELECT * FROM products WHERE product_price > 200
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 2)

# выбираем товары с ценой меньше 300
select_query = """
SELECT * FROM products WHERE product_price < 300
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 3)

# выбираем товары с ценой между 100 и 300
select_query = """
SELECT * FROM products WHERE product_price BETWEEN 100 AND 300
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 4)

# создаем таблицу orders
create_table_query = """
CREATE TABLE orders (
    order_id INT,
    user_id INT,
    product_id INT,
    quantity INT,
    order_date STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
"""
cursor.execute(create_table_query)

# загружаем данные из файла в таблицу orders
load_data_query = """
LOAD DATA INPATH '/user/sasha/warehouse/orders.csv'
OVERWRITE INTO TABLE orders
"""
cursor.execute(load_data_query)


# функция для сохранения результатов запроса в HDFS-каталоге
def save_results(output_directory, query, result_num):
    save_query = f"""
    INSERT OVERWRITE DIRECTORY '{output_directory}/result_{result_num}'
    {query}
    """
    cursor.execute(save_query)


# выбираем все записи из таблицы orders
select_query = """
SELECT * FROM orders
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 5)

# выбираем заказы с датой больше 2023-05-01
select_query = """
SELECT * FROM orders WHERE order_date > '2023-05-01'
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 6)

# выбираем заказы пользователя с id=1002
select_query = """
SELECT * FROM orders WHERE user_id = 1002
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 7)

# создаем таблицу customers
create_table_query = """
CREATE TABLE customers (
    customer_id INT,
    customer_name STRING,
    customer_email STRING,
    product_id INT,
    order_date STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
"""
cursor.execute(create_table_query)

# загружаем данные из файла в таблицу customers
load_data_query = """
LOAD DATA INPATH '/user/sasha/warehouse/customers.csv'
OVERWRITE INTO TABLE customers
"""
cursor.execute(load_data_query)


# функция для сохранения результатов запроса в HDFS-каталоге
def save_results(output_directory, query, result_num):
    save_query = f"""
    INSERT OVERWRITE DIRECTORY '{output_directory}/result_{result_num}'
    {query}
    """
    cursor.execute(save_query)


# выбираем все записи из таблицы customers
select_query = """
SELECT * FROM customers
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 8)

# добавляем запросы
# 1. Выбираем имена всех клиентов из таблицы customers
select_names_query = """
SELECT customer_name
FROM customers
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 9)

# 2. Выбираем id и email клиентов, чьи имена начинаются на "J"
select_j_query = """
SELECT customer_id, customer_email
FROM customers
WHERE customer_name LIKE 'J%'
"""
cursor.execute(select_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, select_query, 10)

# выбираем название товара, цену и количество из заказов
join_query = """
SELECT p.product_name, p.product_price, SUM(o.quantity) as total_quantity
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.product_name, p.product_price
"""
cursor.execute(join_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, join_query, 11)

join_query = """
SELECT c.customer_name, c.customer_email, p.product_name, p.product_price
FROM customers c
JOIN products p
ON c.product_id = p.product_id
"""
cursor.execute(join_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, join_query, 12)

join_query = """
SELECT *
FROM customers
JOIN orders
ON customers.product_id = orders.product_id
AND customers.order_date = orders.order_date
"""

cursor.execute(join_query)
# сохраняем результаты запроса в HDFS-каталоге
output_directory = "/user/sasha/warehouse/test"
save_results(output_directory, join_query, 13)
