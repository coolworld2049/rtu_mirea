SELECT * FROM products WHERE product_price > 200;

SELECT * FROM orders WHERE order_date > '2023-10-18';

SELECT customer_name FROM customers;

SELECT customer_id, customer_email FROM customers WHERE customer_name LIKE 'J%';

SELECT p.product_name, p.product_price, SUM(o.quantity) as total_quantity
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name, p.product_price;

SELECT c.customer_name, c.customer_email, p.product_name, p.product_price
FROM customers c
JOIN products p ON c.product_id = p.product_id;

SELECT * FROM customers
JOIN orders ON customers.product_id = orders.product_id AND customers.order_date = orders.order_date;
