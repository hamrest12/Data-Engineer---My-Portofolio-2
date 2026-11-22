
import streamlit as st
import pandas as pd
import plotly.express as px

from config import get_clickhouse_client

st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Olist E-Commerce Analytics")
st.caption("Data source: ClickHouse | Database: olist_gold")

TABLES = [
    "dim_customers",
    "dim_date",
    "dim_products",
    "dim_sellers",
    "fct_order_items",
    "fct_orders",
    "fct_payments",
    "fct_reviews",
]

@st.cache_resource
def get_client():
    return get_clickhouse_client()

@st.cache_data(ttl=300)
def get_data(query):
    return get_client().query_df(query)

def get_columns(table):
    return get_data(f"""
        SELECT name, type
        FROM system.columns
        WHERE database = 'olist_gold'
          AND table = '{table}'
        ORDER BY position
    """)

def find_column(columns, candidates):
    available = {str(c).lower(): c for c in columns}

    for candidate in candidates:
        if candidate.lower() in available:
            return available[candidate.lower()]

    return None

def get_count(table):
    result = get_data(
        f"SELECT count() AS total FROM olist_gold.{table}"
    )
    return int(result.iloc[0]["total"])

def get_order_filters():
    columns_df = get_columns("fct_orders")
    columns = columns_df["name"].tolist()

    date_col = find_column(columns, [
        "order_purchase_timestamp",
        "purchase_timestamp",
        "order_date",
        "purchase_date"
    ])

    status_col = find_column(columns, [
        "order_status",
        "status"
    ])

    return date_col, status_col

def build_order_filter(date_col, status_col):
    conditions = []

    if date_col and "date_range" in st.session_state:
        start_date, end_date = st.session_state.date_range

        conditions.append(
            f"toDate({date_col}) BETWEEN "
            f"toDate('{start_date}') AND toDate('{end_date}')"
        )

    if status_col and st.session_state.get("selected_status"):
        statuses = ", ".join(
            "'" + s.replace("'", "''") + "'"
            for s in st.session_state.selected_status
        )
        conditions.append(f"{status_col} IN ({statuses})")

    return " AND ".join(conditions) if conditions else "1=1"

# Sidebar
st.sidebar.header("Filter Dashboard")

date_col, status_col = get_order_filters()

if date_col:
    date_data = get_data(f"""
        SELECT
            min(toDate({date_col})) AS min_date,
            max(toDate({date_col})) AS max_date
        FROM olist_gold.fct_orders
    """)

    min_date = date_data.iloc[0]["min_date"]
    max_date = date_data.iloc[0]["max_date"]

    if pd.notna(min_date) and pd.notna(max_date):
        st.sidebar.date_input(
            "Rentang Tanggal",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="date_range"
        )

if status_col:
    status_data = get_data(f"""
        SELECT DISTINCT {status_col}
        FROM olist_gold.fct_orders
        WHERE {status_col} IS NOT NULL
        ORDER BY {status_col}
    """)

    statuses = status_data.iloc[:, 0].dropna().tolist()

    st.sidebar.multiselect(
        "Status Pesanan",
        options=statuses,
        default=statuses,
        key="selected_status"
    )

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

where_clause = build_order_filter(date_col, status_col)

# KPI
st.subheader("Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

filtered_orders = get_data(f"""
    SELECT count() AS total
    FROM olist_gold.fct_orders
    WHERE {where_clause}
""").iloc[0]["total"]

total_customers = get_count("dim_customers")
total_products = get_count("dim_products")
total_sellers = get_count("dim_sellers")

kpi1.metric("Total Orders", f"{filtered_orders:,}")
kpi2.metric("Total Customers", f"{total_customers:,}")
kpi3.metric("Total Products", f"{total_products:,}")
kpi4.metric("Total Sellers", f"{total_sellers:,}")

st.divider()

# Monthly Order Trend
st.subheader("📈 Monthly Order Trend")

if date_col:
    trend = get_data(f"""
        SELECT
            toStartOfMonth({date_col}) AS month,
            count() AS total_orders
        FROM olist_gold.fct_orders
        WHERE {where_clause}
        GROUP BY month
        ORDER BY month
    """)

    if not trend.empty:
        fig = px.line(
            trend,
            x="month",
            y="total_orders",
            markers=True,
            title="Monthly Orders"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data untuk filter yang dipilih.")
else:
    st.warning("Kolom tanggal tidak ditemukan di fct_orders.")

# Order Status
if status_col:
    st.subheader("📦 Order Status Distribution")

    status_chart = get_data(f"""
        SELECT
            {status_col} AS status,
            count() AS total
        FROM olist_gold.fct_orders
        WHERE {where_clause}
        GROUP BY status
        ORDER BY total DESC
    """)

    if not status_chart.empty:
        fig = px.bar(
            status_chart,
            x="status",
            y="total",
            title="Orders by Status"
        )
        st.plotly_chart(fig, use_container_width=True)


# Product Analysis
st.divider()
st.subheader("🏆 Top 10 Products")

product_columns = get_columns("fct_order_items")["name"].tolist()

product_col = find_column(product_columns, [
    "product_id"
])

quantity_col = find_column(product_columns, [
    "order_item_id",
    "quantity",
    "item_quantity"
])

if product_col:
    if quantity_col and quantity_col != "order_item_id":
        product_metric = f"sum({quantity_col})"
    else:
        product_metric = "count()"

    top_products = get_data(f"""
        SELECT
            {product_col} AS product,
            {product_metric} AS total_sold
        FROM olist_gold.fct_order_items
        GROUP BY product
        ORDER BY total_sold DESC
        LIMIT 10
    """)

    if not top_products.empty:
        fig = px.bar(
            top_products,
            x="total_sold",
            y="product",
            orientation="h",
            title="Top 10 Products by Sales Volume"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Kolom product_id tidak ditemukan.")

# Payment Analysis
st.subheader("💳 Payment Method Distribution")

payment_columns = get_columns("fct_payments")["name"].tolist()

payment_type_col = find_column(payment_columns, [
    "payment_type"
])

if payment_type_col:
    payment_data = get_data(f"""
        SELECT
            {payment_type_col} AS payment_method,
            count() AS total_transactions
        FROM olist_gold.fct_payments
        GROUP BY payment_method
        ORDER BY total_transactions DESC
    """)

    if not payment_data.empty:
        fig = px.pie(
            payment_data,
            names="payment_method",
            values="total_transactions",
            title="Payment Methods"
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Kolom payment_type tidak ditemukan.")

# Review Analysis
st.subheader("⭐ Customer Review Distribution")

review_columns = get_columns("fct_reviews")["name"].tolist()

score_col = find_column(review_columns, [
    "review_score"
])

if score_col:
    review_data = get_data(f"""
        SELECT
            {score_col} AS review_score,
            count() AS total_reviews
        FROM olist_gold.fct_reviews
        WHERE {score_col} IS NOT NULL
        GROUP BY review_score
        ORDER BY review_score
    """)

    if not review_data.empty:
        fig = px.bar(
            review_data,
            x="review_score",
            y="total_reviews",
            title="Customer Review Scores",
            labels={
                "review_score": "Review Score",
                "total_reviews": "Number of Reviews"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Kolom review_score tidak ditemukan.")


# Data Explorer
st.divider()
st.subheader("🔎 Gold Data Explorer")

selected_table = st.selectbox(
    "Pilih tabel",
    TABLES
)

limit = st.selectbox(
    "Jumlah baris",
    [10, 50, 100, 500]
)

preview = get_data(f"""
    SELECT *
    FROM olist_gold.{selected_table}
    LIMIT {limit}
""")

st.dataframe(preview, use_container_width=True)

st.caption(
    "Olist Data Engineering Portfolio | "
    "ClickHouse + dbt + Airflow + Streamlit"
)
