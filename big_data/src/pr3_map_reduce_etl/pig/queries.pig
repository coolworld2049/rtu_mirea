CustomerOrders = JOIN orders BY customer_id, products BY product_id;
Result = FOREACH CustomerOrders GENERATE orders.order_id, orders.order_date, products.product_name, products.price;
DUMP Result;
