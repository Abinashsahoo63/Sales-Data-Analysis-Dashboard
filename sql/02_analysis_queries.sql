USE sales_analysis;

-- KPI: Total revenue
SELECT ROUND(SUM(quantity * unit_price * (1 - discount_percent / 100)), 2) AS total_revenue
FROM sales;

-- KPI: Total distinct orders
SELECT COUNT(DISTINCT order_id) AS total_orders FROM sales;

-- KPI: Units sold
SELECT SUM(quantity) AS units_sold FROM sales;

-- Monthly revenue trend (line chart)
SELECT DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
       ROUND(SUM(quantity * unit_price * (1 - discount_percent / 100)), 2) AS revenue
FROM sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month;

-- Revenue by category (bar chart)
SELECT category,
       ROUND(SUM(quantity * unit_price * (1 - discount_percent / 100)), 2) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- Revenue by region
SELECT region,
       ROUND(SUM(quantity * unit_price * (1 - discount_percent / 100)), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- Top five products by revenue
SELECT product,
       ROUND(SUM(quantity * unit_price * (1 - discount_percent / 100)), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;

-- Average order value
SELECT ROUND(
  SUM(quantity * unit_price * (1 - discount_percent / 100)) /
  NULLIF(COUNT(DISTINCT order_id), 0), 2
) AS average_order_value
FROM sales;

-- Monthly category breakdown
SELECT DATE_FORMAT(order_date, '%Y-%m') AS sales_month, category,
       ROUND(SUM(quantity * unit_price * (1 - discount_percent / 100)), 2) AS revenue
FROM sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m'), category
ORDER BY sales_month, category;

-- Basic data quality check
SELECT * FROM sales
WHERE quantity <= 0 OR unit_price < 0 OR discount_percent < 0 OR discount_percent > 100;
