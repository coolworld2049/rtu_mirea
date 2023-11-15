-- 1
SELECT * FROM customers WHERE customer_name like "%Johnson%";

-- 2
SELECT * FROM customers WHERE customer_name LIKE 'J%';

-- 3
SELECT * FROM orders WHERE order_date > '2023-10-18';

-- 4
SELECT * FROM products WHERE product_price > 150;

-- 5
SELECT p.product_name, p.product_price, SUM(o.quantity) as total_quantity
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name, p.product_price;

-- 6
SELECT * FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
WHERE customers.customer_name = 'Mia Johnson';
