from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

checks = [
    ("olist_orders_dataset.csv", "order_id"),
    ("olist_customers_dataset.csv", "customer_id"),
    ("olist_products_dataset.csv", "product_id"),
    ("olist_sellers_dataset.csv", "seller_id")
]

for file_name, key_columns in checks:
    file_path = RAW_DIR / file_name
    df = pd.read_csv(file_path)

    duplicate_count = int(
        df[key_columns].duplicated().sum()
    )

    null_count = int(
        df[key_columns].isna().sum()
    )

    print(f"\nFile : {file_name}")
    print(f"Key : {key_columns}")
    print(f"Duplicate : {duplicate_count}")
    print(f"Null : {null_count}")