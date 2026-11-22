from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
product = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
sellers = pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv")

print("="*70)
print("RELATION CHECK")
print("="*70)

# Order yang tidak memiliki customer
missing_customer = ~orders["customer_id"].isin(customers["customer_id"])
print("Order tanpa customer yang cocok:", int(missing_customer.sum()))

# Item dengan order yang tidak ditemukan
missing_order = ~items["order_id"].isin(orders["order_id"])
print("Order item tanpa order yang cocok:", int(missing_order.sum()))

# Item dengan product yang tidak ditemukan
missing_product = ~items["product_id"].isin(product["product_id"])
print("Order item tanpa product yang cocok:", int(missing_product.sum()))

# Item dengan seller yang tidak ditemukan
missing_seller = ~items["seller_id"].isin(sellers["seller_id"])
print("Order item tanpa seller yang cocok:", int(missing_seller.sum()))

# Rata-rata item per order
items_per_order = items.groupby("order_id").size()
print("Rata-rata item row per order:", round(items_per_order.mean(), 2))
print("Order dengan lebih dari satu item row:", int((items_per_order > 1).sum()))