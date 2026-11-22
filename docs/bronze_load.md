<WritingBlock id="58322" variant="document">
# Bronze Layer Load Documentation

Overview
The Olist raw CSV files are loaded into ClickHouse using Python and clickhouse-connect.
Source
- Source directory: data/raw/
- Source format: CSV
- Destination database: olist_warehouse
- Destination tables: bronze_*
- ClickHouse engine: MergeTree
Load Strategy
The Bronze load uses a full reload strategy:
1. Read CSV column names.
2. Create the Bronze table if it does not exist.
3. Truncate the existing table.
4. Read the CSV in chunks.
5. Insert each chunk into ClickHouse.
6. Validate the final row count.

Data Types
All Bronze columns use Nullable(String).

Data type conversion and business validation will be handled in downstream dbt models.
Validation Results
Table	CSV Rows	ClickHouse Rows	Match
bronze_orders			
bronze_order_items			
bronze_customers			
bronze_products			
bronze_sellers			
bronze_order_payments			
bronze_order_reviews			
bronze_geolocation			
bronze_category_translation			

Idempotency Test
- First load completed:
- Second load completed:
- Row counts remained unchanged:
- Duplicate rows introduced by rerun: No
Result
The Olist raw CSV files have been loaded into ClickHouse Bronze tables.
</WritingBlock>