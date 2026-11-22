
{{
    config(
        materialized = 'table',
        schema = 'olist_gold',
        engine = 'MergeTree()',
        order_by = 'order_id'
    )
}}

SELECT
    order_id,
    customer_id,
    order_status,

    toDate(order_purchase_timestamp) AS order_purchase_date,

    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,

    dateDiff(
        'day',
        order_purchase_timestamp,
        order_delivered_customer_date
    ) AS actual_delivery_days,

    dateDiff(
        'day',
        order_purchase_timestamp,
        order_estimated_delivery_date
    ) AS estimated_delivery_days

FROM {{ ref('stg_orders') }}
