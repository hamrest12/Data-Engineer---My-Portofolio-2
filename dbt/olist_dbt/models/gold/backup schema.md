
version: 2

models:
  - name: dim_customers
    description: Dimension table yang menyimpan informasi unik setiap customer
      untuk analisis transaksi Olist.
    columns:
      - name: customer_id
        description: Unique identifier untuk customer.
        data_tests:
          - not_null
          - unique
      - name: customer_unique_id
        description: Identifier unik customer lintas transaksi.

  - name: dim_products
    description: Dimension table yang menyimpan informasi produk
      untuk analisis penjualan.
    columns:
      - name: product_id
        description: Unique identifier untuk produk.
        data_tests:
          - not_null
          - unique
      - name: product_category_name
        description: Kategori produk.

  - name: dim_sellers
    description: "Seller dimension"
    columns:
      - name: seller_id
        data_tests:
          - not_null
          - unique

  - name: dim_date
    description: "Calendar date dimension"
    columns:
      - name: date_day
        data_tests:
          - not_null
          - unique

  - name: fct_orders
    description: "One row per order"
    columns:
      - name: order_id
        data_tests:
          - not_null
          - unique

      - name: customer_id
        data_tests:
          - not_null
          - relationships:
             arguments:
              to: ref('dim_customers')
              field: customer_id

      - name: order_purchase_date
        data_tests:
          - not_null

  - name: fct_order_items
    description: "One row per order item"
    columns:
      - name: order_id
        data_tests:
          - not_null
          - relationships:
             arguments:
              to: ref('fct_orders')
              field: order_id
      - name: order_item_id
        data_tests:
          - not_null
      - name: product_id
        data_tests:
          - not_null
      - name: seller_id
        data_tests:
          - not_null

  - name: fct_payments
    description: "One row per payment record"
    columns:
      - name: order_id
        data_tests:
          - not_null
          - relationships:
             arguments:
              to: ref('fct_orders')
              field: order_id
      - name: payment_sequential
        data_tests:
          - not_null

  - name: fct_reviews
    description: "One row per review record"
    columns:
      - name: review_id
        data_tests:
          - not_null
      - name: order_id
        data_tests:
          - not_null

