# 🛒 Ecommerce Analytics (SQL + Tableau)

## 📌 Project Overview
This project analyzes an e-commerce transactions dataset to uncover revenue trends, top-selling products, and customer purchasing behavior.  
The analysis combines **SQL** for data querying with **Tableau** for visualization.  

## ⚙️ Tools & Skills
- SQL (joins, aggregations, window functions)
- Tableau Public (interactive dashboards)
- Data Cleaning & Transformation

## 📂 Dataset
- **Source:** [Kaggle – Online Retail Dataset](https://www.kaggle.com/datasets/vijayuv/onlineretail)  
- ~500k rows of transaction data (Invoice ID, Product, Quantity, Price, Customer ID, Date).  

## 🔑 Key Questions
1. What are the weekly and monthly revenue trends?  
2. Which products generate the most revenue?  
3. How do repeat customers differ from one-time buyers?  
4. Are there seasonal spikes in sales?  

## 📊 Dashboard
- **Link:** [E-Commerce Sales & Customer Insights Dashboard](https://public.tableau.com/views/E-CommerceSalesCustomerInsightsDashboard/SalesInsightsDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## 📝 Example SQL Queries
```sql
-- Weekly Revenue Trend
SELECT DATE_TRUNC('week', invoice_date) AS week_start,
       SUM(quantity * unit_price) AS revenue
FROM ecommerce_orders
GROUP BY 1
ORDER BY 1;

-- Top 10 Products by Revenue
SELECT description, SUM(quantity * unit_price) AS total_revenue
FROM ecommerce_orders
GROUP BY description
ORDER BY total_revenue DESC
LIMIT 10;
