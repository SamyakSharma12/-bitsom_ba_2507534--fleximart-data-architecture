-- Query 1: Customer Purchase History
-- Business Question: "Generate a detailed report showing each customer's name, email,
-- total number of orders placed, and total amount spent. Include only customers who have
-- placed at least 2 orders and spent more than ₹5,000. Order by total amount spent in descending order."
-- Must join: customers, orders, order_items (orders total already stores header total)
-- Output: customer_name | email | total_orders | total_spent

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
HAVING COUNT(DISTINCT o.order_id) >= 2
   AND SUM(o.total_amount) > 5000
ORDER BY total_spent DESC;

-- Query 2: Product Sales Analysis
-- Business Question: "For each product category, show the category name, number of different
-- products sold, total quantity sold, and total revenue generated. Only include categories
-- that have generated more than ₹10,000 in revenue. Order by total revenue descending."
-- Must join: products, order_items (via orders to filter Completed)
-- Output: category | num_products | total_quantity_sold | total_revenue

SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS num_products,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.subtotal), 2) AS total_revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
HAVING SUM(oi.subtotal) > 10000
ORDER BY total_revenue DESC;

-- Query 3: Monthly Sales Trend (2024)
-- Business Question: "Show monthly sales trends for the year 2024. For each month,
-- display the month name, total number of orders, total revenue, and the running total of revenue."
-- Use window function for running total; MySQL 8+ syntax.
-- Output: month_name | total_orders | monthly_revenue | cumulative_revenue

SELECT
    MONTHNAME(o.order_date) AS month_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS monthly_revenue,
    ROUND(SUM(SUM(o.total_amount)) OVER (ORDER BY MONTH(o.order_date)), 2) AS cumulative_revenue
FROM orders o
WHERE o.status = 'Completed'
  AND YEAR(o.order_date) = 2024
GROUP BY MONTH(o.order_date), MONTHNAME(o.order_date)
ORDER BY MONTH(o.order_date);
