-- Выбрать все данные из таблицы products
SELECT * FROM products;

-- Продукты с ценой больше 200
SELECT * FROM products WHERE product_price > 200;

-- Все данные из таблицы orders
SELECT * FROM orders;

-- Заказы после определенной даты
SELECT * FROM orders WHERE order_date > '2023-10-18';

-- Все данные из таблицы customers
SELECT * FROM customers;

-- Имена клиентов
SELECT customer_name FROM customers;

-- Детали клиентов с именами, начинающимися с 'J'
SELECT customer_id, customer_email FROM customers WHERE customer_name LIKE 'J%';

-- Агрегированные данные из таблиц orders и products
SELECT p.product_name, p.product_price, SUM(o.quantity) as total_quantity
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name, p.product_price;

-- Таблицы customers и products
SELECT c.customer_name, c.customer_email, p.product_name, p.product_price
FROM customers c
JOIN products p ON c.product_id = p.product_id;

-- Таблицы customers и orders на основе product_id и order_date
SELECT * FROM customers
JOIN orders ON customers.product_id = orders.product_id AND customers.order_date = orders.order_date;
