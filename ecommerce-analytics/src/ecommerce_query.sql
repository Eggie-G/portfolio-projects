-- Change the path to your actual file:
CREATE OR REPLACE VIEW orders AS
SELECT
  CAST(NULLIF(invoice_no,'') AS VARCHAR) AS invoice_id,
  STRPTIME(invoice_date, '%m/%d/%Y %H:%M') AS order_date,
  TRY_CAST(customer_id AS BIGINT) AS customer_id,
  CAST(country AS VARCHAR)                AS country,
  CAST(stock_code AS VARCHAR)             AS product_id,
  CAST(description AS VARCHAR)            AS description,
  CAST(quantity AS INTEGER)               AS quantity,
  CAST(unit_price AS DOUBLE)              AS unit_price,
  (quantity * unit_price)                 AS revenue
FROM read_csv_auto('../data/online_retail_data.csv');


-- ===== 1) Weekly revenue + 4-week moving average =====
WITH weekly AS (
  SELECT
    DATE_TRUNC('week', order_date) AS week_start,
    SUM(revenue)                   AS revenue
  FROM orders
  GROUP BY 1
)
SELECT
  week_start,
  revenue,
  AVG(revenue) OVER (
    ORDER BY week_start
    ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
  ) AS revenue_4wk_ma
FROM weekly
ORDER BY week_start;


-- ===== 2) Top 10 products by revenue =====
SELECT
  description,
  SUM(revenue) AS total_revenue,
  SUM(quantity) AS units
FROM orders
GROUP BY description
ORDER BY total_revenue DESC
LIMIT 10;


-- ===== 3) Country KPIs (Revenue, Orders, Customers, AOV) =====
SELECT
  country,
  SUM(revenue)                                   AS revenue,
  COUNT(DISTINCT invoice_id)                      AS orders,
  COUNT(DISTINCT customer_id)                     AS customers,
  SUM(revenue) * 1.0 / NULLIF(COUNT(DISTINCT invoice_id),0) AS aov
FROM orders
GROUP BY country
ORDER BY revenue DESC;


-- ===== 4) Repeat purchase rate (60-day window) =====
-- Mark customers who purchased again within 60 days of their first order
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_dt
  FROM orders
  GROUP BY 1
),
next_order AS (
  SELECT o.customer_id,
         MIN(o.order_date) AS next_dt
  FROM orders o
  JOIN first_order f USING (customer_id)
  WHERE o.order_date > f.first_dt
  GROUP BY 1
)
SELECT
  COUNT(*) FILTER (WHERE next_dt IS NOT NULL AND next_dt <= first_dt + INTERVAL 60 DAY) * 1.0
  / COUNT(*)                                              AS repeat_within_60d
FROM first_order
LEFT JOIN next_order USING (customer_id);


-- ===== (Optional) Export tidy tables for Tableau =====
-- Uncomment these to write out CSVs you can drag into Tableau
 COPY (
   SELECT * FROM (
     WITH weekly AS (
       SELECT DATE_TRUNC('week', order_date) AS week_start, SUM(revenue) AS revenue
       FROM orders GROUP BY 1
     )
     SELECT week_start, revenue,
            AVG(revenue) OVER (ORDER BY week_start ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS revenue_4wk_ma
     FROM weekly
   )
 ) TO '../data/weekly_revenue.csv' WITH (HEADER, DELIMITER ',');

 COPY (
   SELECT description, SUM(revenue) AS total_revenue, SUM(quantity) AS units
   FROM orders GROUP BY description ORDER BY total_revenue DESC LIMIT 10
 ) TO '../data/top_products.csv' WITH (HEADER, DELIMITER ',');

 COPY (
   SELECT country, SUM(revenue) AS revenue, COUNT(DISTINCT invoice_id) AS orders,
          COUNT(DISTINCT customer_id) AS customers,
          SUM(revenue) * 1.0 / NULLIF(COUNT(DISTINCT invoice_id),0) AS aov
   FROM orders GROUP BY country ORDER BY revenue DESC
 ) TO '../data/country_kpis.csv' WITH (HEADER, DELIMITER ',');
