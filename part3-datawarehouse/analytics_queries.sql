-- Query 1: Monthly Sales Drill-Down Analysis
SELECT
  d.year,
  d.quarter,
  d.month_name,
  SUM(f.total_amount) AS total_sales,
  SUM(f.quantity_sold) AS total_quantity
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.year, d.quarter, d.month, d.month_name
ORDER BY d.year, d.quarter, d.month;

-- Query 2: Top 10 Products by Revenue
WITH product_revenue AS (
  SELECT p.product_name, p.category,
         SUM(f.quantity_sold) AS units_sold,
         SUM(f.total_amount) AS revenue
  FROM fact_sales f
 
