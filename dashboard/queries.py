
from config import get_clickhouse_client


def get_gold_tables():
    """
    Mengambil daftar tabel dalam database Gold.
    """

    client = get_clickhouse_client()

    try:
        result = client.query("""
            SHOW TABLES FROM olist_gold
        """)

        return [row[0] for row in result.result_rows]

    finally:
        client.close()


def get_table_columns(table_name):
    """
    Mengambil nama dan tipe data kolom suatu tabel.
    """

    allowed_tables = {
        "dim_customers",
        "dim_date",
        "dim_products",
        "dim_sellers",
        "fct_order_items",
        "fct_orders",
        "fct_payments",
        "fct_reviews",
    }

    if table_name not in allowed_tables:
        raise ValueError("Nama tabel tidak diizinkan")

    client = get_clickhouse_client()

    try:
        result = client.query(f"""
            DESCRIBE TABLE olist_gold.{table_name}
        """)

        return [
            {
                "column": row[0],
                "type": row[1]
            }
            for row in result.result_rows
        ]

    finally:
        client.close()



def inspect_gold_schema():
    """
    Menampilkan struktur kolom seluruh tabel Gold.
    """

    client = get_clickhouse_client()

    tables = [
        "dim_customers",
        "dim_date",
        "dim_products",
        "dim_sellers",
        "fct_order_items",
        "fct_orders",
        "fct_payments",
        "fct_reviews",
    ]

    try:
        for table in tables:
            print(f"\n{'=' * 60}")
            print(f"TABLE: {table}")
            print("=" * 60)

            result = client.query(
                f"DESCRIBE TABLE olist_gold.{table}"
            )

            for row in result.result_rows:
                column_name = row[0]
                column_type = row[1]

                print(f"{column_name:<40} {column_type}")

    finally:
        client.close()


def inspect_gold_row_counts():
    """
    Mengambil jumlah baris seluruh tabel Gold.
    """

    client = get_clickhouse_client()

    tables = [
        "dim_customers",
        "dim_date",
        "dim_products",
        "dim_sellers",
        "fct_order_items",
        "fct_orders",
        "fct_payments",
        "fct_reviews",
    ]

    try:
        for table in tables:
            result = client.query(
                f"SELECT count() FROM olist_gold.{table}"
            )

            total_rows = result.result_rows[0][0]

            print(f"{table:<25} : {total_rows:,} rows")

    finally:
        client.close()


def get_kpi_data():
    """
    Mengambil KPI utama dari database Gold.
    Query final akan ditambahkan setelah validasi kolom.
    """

    client = get_clickhouse_client()

    try:
        # Validasi tabel yang dibutuhkan
        tables = [
            "dim_customers",
            "fct_orders",
            "fct_order_items",
        ]

        for table in tables:
            result = client.query(
                f"SELECT count() FROM olist_gold.{table}"
            )

            print(
                f"{table}: "
                f"{result.result_rows[0][0]:,} rows"
            )

    finally:
        client.close()
