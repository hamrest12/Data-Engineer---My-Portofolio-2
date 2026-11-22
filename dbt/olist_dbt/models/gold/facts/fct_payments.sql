
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
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value

FROM {{ ref('stg_order_payments') }}
