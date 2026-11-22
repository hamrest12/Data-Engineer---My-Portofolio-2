
# Olist Data Warehouse Design

## 1. Architecture

The project uses a three-layer data warehouse architecture:

- Bronze: raw Olist CSV data stored in ClickHouse.
- Silver: cleaned, standardized, and validated data built with dbt.
- Gold: business-ready fact and dimension models.

## 2. Database Structure

| Database | Purpose |
|---|---|
| olist_warehouse | Bronze source tables |
| olist_silver | Silver transformation models |
| olist_gold | Gold analytical models |

## 3. Gold Fact Tables

| Model | Grain |
|---|---|
| fct_orders | One row per order_id |
| fct_order_items | One row per order_id + order_item_id |
| fct_payments | One row per payment record |
| fct_reviews | One row per review_id |

## 4. Gold Dimension Tables

| Model | Grain |
|---|---|
| dim_customers | One row per customer_id |
| dim_products | One row per product_id |
| dim_sellers | One row per seller_id |
| dim_date | One row per calendar date |

## 5. Important Relationships

- fct_orders.customer_id -> dim_customers.customer_id
- fct_orders.order_id -> fct_order_items.order_id
- fct_orders.order_id -> fct_payments.order_id
- fct_orders.order_id -> fct_reviews.order_id
- fct_order_items.product_id -> dim_products.product_id
- fct_order_items.seller_id -> dim_sellers.seller_id
- fct_orders.order date -> dim_date.date

## 6. Design Principles

- Define the grain before building each model.
- Avoid duplicate counting when joining fact tables.
- Keep raw source data in Bronze.
- Perform type conversion and data cleaning in Silver.
- Build business metrics in Gold.
- Validate key uniqueness and relationship integrity.
- Use ClickHouse-appropriate table engines and sorting keys.

## 7. Validation Results

| Check | Result |
|---|---|
| Order ID uniqueness | |
| Order item composite-key uniqueness | |
| Payment grain reviewed | |
| Required order fields checked | |
| Sample data reviewed | |
