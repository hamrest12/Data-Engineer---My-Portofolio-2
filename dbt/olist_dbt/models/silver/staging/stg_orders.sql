{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = 'order_id'
    )
}}

SELECT 
    assumeNotNull(
        nullIf(trimBoth(order_id), '')
    ) AS order_id,
    nullIf(trimBoth(customer_id), '') AS customer_id,

    lowerUTF8(
        nullIf(trimBoth(order_status), '')
    ) AS order_status,

    parseDateTimeBestEffortOrNull(
        nullIf(trimBoth(order_purchase_timestamp), '')
    ) AS order_purchase_timestamp,

    parseDateTimeBestEffortOrNull(
        nullIf(trimBoth(order_approved_at), '')
    ) AS order_approved_at,

    parseDateTimeBestEffortOrNull(
        nullIf(trimBoth(order_delivered_carrier_date), '')
    ) AS order_delivered_carrier_date,

    parseDateTimeBestEffortOrNull(
        nullIf(trimBoth(order_delivered_customer_date), '')
    ) AS order_delivered_customer_date,

    parseDateTimeBestEffortOrNull(
        nullIf(trimBoth(order_estimated_delivery_date), '')
    ) AS order_estimated_delivery_date

FROM {{ source('olist_bronze', 'bronze_orders') }}
WHERE
    nullIf(trimBoth(order_id), '') IS NOT NULL
