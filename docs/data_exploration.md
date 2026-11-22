
# Olist Dataset Exploration

## 1. Dataset Overview

- Dataset: Brazilian E-Commerce Public Dataset by Olist
- Source: Kaggle
- Exploration tool: Python, pandas
- Data warehouse: ClickHouse

## 2. Table Summary

| Table | Row Count | Column Count |
|---|---:|---:|
| orders | | |
| order_items | | |
| customers | | |
| products | | |
| sellers | | |
| order_payments | | |
| order_reviews | | |
| geolocation | | |
| product_category_translation | | |

## 3. Key Findings

- Candidate key for orders: `order_id`
- Candidate key for customers: `customer_id`
- Candidate key for products: `product_id`
- Candidate key for sellers: `seller_id`
- Order items can contain multiple rows per `order_id`.
- One customer can place multiple orders.

## 4. Data Quality Findings

- Missing values:
- Duplicate keys:
- Unmatched relationships:
- Invalid date values:
- Other observations:

## 5. Next Steps

The next stage is to load the raw Olist CSV files into ClickHouse Bronze tables.
