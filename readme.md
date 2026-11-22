# Olist E-Commerce Data Engineering Pipeline

An end-to-end Data Engineering portfolio project built using **ClickHouse, Python, dbt, Apache Airflow, Docker, and Streamlit**.

This project processes the Brazilian Olist e-commerce dataset through a data pipeline, from raw CSV ingestion to analytical data models and interactive visualization.

## Project Overview

The pipeline implements a Medallion Architecture:

- **Bronze:** Raw Olist CSV data loaded into ClickHouse.
- **Silver:** Cleaned and transformed data using dbt.
- **Gold:** Analytical fact and dimension tables designed for reporting and visualization.

Apache Airflow orchestrates the pipeline automatically.

## Architecture

```text
Olist CSV Dataset
       |
       v
Python Data Loader
       |
       v
ClickHouse - Bronze
       |
       v
dbt Transformations
       |
       v
ClickHouse - Silver
       |
       v
dbt Transformations
       |
       v
ClickHouse - Gold
       |
       v
Streamlit + Plotly Dashboard
```

Apache Airflow orchestrates the Bronze, Silver, and Gold pipeline tasks.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data ingestion |
| ClickHouse | Analytical database |
| Docker | Containerization |
| dbt | Data transformation |
| Apache Airflow | Workflow orchestration |
| Streamlit | Dashboard application |
| Plotly | Data visualization |
| Git & GitHub | Version control |

## Data Models

### Gold Dimensions
- dim_customers
- dim_date
- dim_products
- dim_sellers

### Gold Facts
- fct_orders
- fct_order_items
- fct_payments
- fct_reviews

## Pipeline Workflow

1. Load Olist CSV files into Bronze tables.
2. Transform raw data into Silver models using dbt.
3. Build analytical Gold models using dbt.
4. Orchestrate all pipeline tasks using Apache Airflow.
5. Visualize Gold data using Streamlit and Plotly.

## Airflow Schedule

The pipeline is configured to run daily at 00:00 Asia/Jakarta time.

DAG: `olist_data_pipeline`

## Dashboard Features

- Total orders, customers, products, and sellers.
- Monthly order trends.
- Order status distribution.
- Top 10 products.
- Payment method distribution.
- Customer review score distribution.
- Date and order status filters.
- Gold table data explorer.

## Project Validation

Gold model row counts from the completed pipeline:

| Table | Rows |
|---|---:|
| dim_customers | 99,441 |
| dim_date | 774 |
| dim_products | 32,951 |
| dim_sellers | 3,095 |
| fct_orders | 99,441 |
| fct_order_items | 112,650 |
| fct_payments | 103,886 |
| fct_reviews | 99,224 |

## Screenshots

Dashboard screenshots will be available in `docs/screenshots/`.

## Project Structure

```text
├── airflow/
│   └── dags/
├── data/
│   └── raw/
├── dbt/
│   └── olist_dbt/
├── docker/
├── docs/
│   ├── architecture/
│   └── screenshots/
├── scr/
├── dashboard/
└── README.md
```

## Security

Credentials and environment variables are stored in `.env` files and should never be committed to GitHub.

## Author

Data Engineering Portfolio Project

**Focus:** Data Engineering, ETL/ELT, Data Modeling, Workflow Orchestration, and Analytics.
