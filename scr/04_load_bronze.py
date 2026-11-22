from pathlib import Path
import pandas as pd
import clickhouse_connect

# =========================================================
# CONFIGURATION
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

CLICKHOUSE_HOST = "clickhouse"
CLICKHOUSE_PORT = 8123
CLICKHOUSE_DATABASE = "olist_clickhouse"
CLICKHOUSE_USER = "clickhouse"
CLICKHOUSE_PASSWORD = "adminpass123"

CHUNK_SIZE = 10_000

# CSV filename -> ClickHouse table name
TABLE_MAPPING = {
    "olist_orders_dataset.csv": "bronze_orders",
    "olist_order_items_dataset.csv": "bronze_order_items",
    "olist_customers_dataset.csv": "bronze_customers",
    "olist_products_dataset.csv": "bronze_products",
    "olist_sellers_dataset.csv": "bronze_sellers",
    "olist_order_payments_dataset.csv": "bronze_order_payments",
    "olist_order_reviews_dataset.csv": "bronze_order_reviews",
    "olist_geolocation_dataset.csv": "bronze_geolocation",
    "product_category_name_translation.csv": "bronze_category_translation",
}

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def quote_identifier(identifier: str) -> str:
    """
    Safely quote a ClickHouse database/table/column identifier.
    """
    escaped = identifier.replace("`", "``")
    return f"`{escaped}`"

def create_bronze_table(client, database: str, table_name: str, columns: list[str],) -> None:
    """
    Create a Bronze table with Nullable(String) columns.
    """
    column_definitions = ",\n".join(
        f"{quote_identifier(column)} Nullable(String)"
        for column in columns
    )

    query = f"""
    CREATE TABLE IF NOT EXISTS
        {quote_identifier(database)}.{quote_identifier(table_name)}
    (
        {column_definitions}
    )
    ENGINE = MergeTree
    ORDER BY tuple()
    """

    client.command(query)

def normalize_chunk(df: pd.DataFrame) -> list[tuple]:
    """
    Convert pandas values into Python strings or None.

    Empty/NA values become None, which maps to NULL
    for Nullable(String) columns.
    """
    df = df.astype(object)
    df = df.where(pd.notna(df), None)

    rows = []

    for row in df.itertuples(index=False, name=None):
        normalized_row = tuple(
            None if value is None else str(value)
            for value in row
        )
        rows.append(normalized_row)

    return rows

def load_csv(client, csv_path: Path, database: str, table_name: str) -> int:
    """
    Full reload one CSV into a Bronze table.

    The table is truncated before loading to avoid
    duplicate rows when this script is run again.
    """
    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}"
        )

    # Read column names without loading the whole CSV
    header_df = pd.read_csv(csv_path, nrows=0, encoding="utf-8",)
    columns = header_df.columns.tolist()

    # Create the table if it does not exist
    create_bronze_table(client=client, database=database, table_name=table_name, columns=columns)

    full_table_name = (
        f"{quote_identifier(database)}."
        f"{quote_identifier(table_name)}"
    )

    # Full reload strategy
    client.command(f"TRUNCATE TABLE {full_table_name}")
    inserted_rows = 0

    # Read CSV in chunks to control memory usage
    for chunk in pd.read_csv(csv_path, chunksize=CHUNK_SIZE, encoding="utf-8", dtype="string"):
        rows = normalize_chunk(chunk)

        if rows:
            client.insert(
                table=full_table_name,
                data=rows,
                column_names=columns,
            )

            inserted_rows += len(rows)

            print(f"  Inserted {inserted_rows:,} rows " f"into {table_name}")

    return inserted_rows

# =========================================================
# MAIN
# =========================================================

def main():
    print("=" * 70)
    print("OLIST BRONZE LOAD")
    print("=" * 70)

    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
    )

    try:
        # Verify connection
        version = client.query("SELECT version()").result_rows[0][0]

        print(f"Connected to ClickHouse version: {version}")
        print(f"Database: {CLICKHOUSE_DATABASE}")

        total_inserted = 0

        for csv_file, table_name in TABLE_MAPPING.items():
            csv_path = RAW_DIR / csv_file

            print(f"\nLoading: {csv_file}")
            print(f"Target : {table_name}")

            inserted = load_csv(client=client, csv_path=csv_path, database=CLICKHOUSE_DATABASE, table_name=table_name)
            total_inserted += inserted

            print(f"Completed {table_name}: " f"{inserted:,} rows")

        print("\n" + "=" * 70)
        print("BRONZE LOAD COMPLETED")
        print(f"Total rows inserted: {total_inserted:,}")
        print("=" * 70)

    finally:
        client.close()

if __name__ == "__main__":
    main()
