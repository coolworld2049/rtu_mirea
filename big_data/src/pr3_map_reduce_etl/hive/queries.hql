--Выбрать все заказы для конкретного покупателя (с использованием JOIN):
SELECT orders.order_id, orders.order_date, products.product_name, products.price
FROM orders
         JOIN products ON orders.product_id = products.product_id
WHERE orders.customer_id = 1;

--Получить общую сумму заказов для каждого покупателя:
SELECT customers.customer_id, customers.customer_name, SUM(orders.total_amount) AS total_spent
FROM customers
         JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_id, customers.customer_name;

--Выбрать все продукты и количество заказов для каждого продукта:
SELECT products.product_name, COUNT(orders.order_id) AS order_count
FROM products
         LEFT JOIN orders ON products.product_id = orders.product_id
GROUP BY products.product_name;

--Найти всех покупателей, не сделавших заказ:
SELECT customers.customer_id, customers.customer_name
FROM customers
         LEFT JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL;

--Получить среднюю стоимость заказа:
SELECT AVG(orders.total_amount) AS average_order_cost
FROM orders;