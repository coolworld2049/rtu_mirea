from pyhive import hive


def create_table(cursor, table_name, columns, row_format):
    create_table_query = f"""
    CREATE TABLE {table_name} (
        {columns}
    )
    {row_format}
    """
    cursor.execute(create_table_query)


def load_data(cursor, table_name, data_path):
    load_data_query = f"""
    LOAD DATA INPATH '{data_path}'
    OVERWRITE INTO TABLE {table_name}
    """
    cursor.execute(load_data_query)


def save_results(cursor, output_directory, query, result_num):
    save_query = f"""
    INSERT OVERWRITE DIRECTORY '{output_directory}/result_{result_num}'
    {query}
    """
    cursor.execute(save_query)


def main():
    conn = hive.Connection(
        host="localhost", port=10000, username="ivanovnp", database="default"
    )
    cursor = conn.cursor()

    # Create and load products table
    create_table(
        cursor,
        "products",
        "product_id INT, product_name STRING, product_price FLOAT",
        "ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'",
    )
    load_data(cursor, "products", "/user/ivanovnp/warehouse/products.csv")

    # Create and load orders table
    create_table(
        cursor,
        "orders",
        "order_id INT, user_id INT, product_id INT, quantity INT, order_date STRING",
        "ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'",
    )
    load_data(cursor, "orders", "/user/ivanovnp/warehouse/orders.csv")

    # Create and load customers table
    create_table(
        cursor,
        "customers",
        "customer_id INT, customer_name STRING, customer_email STRING, product_id INT, order_date STRING",
        "ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'",
    )
    load_data(cursor, "customers", "/user/ivanovnp/warehouse/customers.csv")

    # Select queries
    select_and_save(
        cursor, "/user/ivanovnp/warehouse/test", "SELECT * FROM products", 1
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT * FROM products WHERE product_price > 200",
        2,
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT * FROM products WHERE product_price < 300",
        3,
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT * FROM products WHERE product_price BETWEEN 100 AND 300",
        4,
    )
    select_and_save(cursor, "/user/ivanovnp/warehouse/test", "SELECT * FROM orders", 5)
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT * FROM orders WHERE order_date > '2023-05-01'",
        6,
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT * FROM orders WHERE user_id = 1002",
        7,
    )
    select_and_save(
        cursor, "/user/ivanovnp/warehouse/test", "SELECT * FROM customers", 8
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT customer_name FROM customers",
        9,
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT customer_id, customer_email FROM customers WHERE customer_name LIKE 'J%'",
        10,
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT p.product_name, p.product_price, SUM(o.quantity) as total_quantity FROM orders o JOIN products p ON o.product_id = p.product_id GROUP BY p.product_name, p.product_price",
        11,
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT c.customer_name, c.customer_email, p.product_name, p.product_price FROM customers c JOIN products p ON c.product_id = p.product_id",
        12,
    )
    select_and_save(
        cursor,
        "/user/ivanovnp/warehouse/test",
        "SELECT * FROM customers JOIN orders ON customers.product_id = orders.product_id AND customers.order_date = orders.order_date",
        13,
    )

    conn.close()


def select_and_save(cursor, output_directory, query, result_num):
    cursor.execute(query)
    save_results(cursor, output_directory, query, result_num)


if __name__ == "__main__":
    main()
