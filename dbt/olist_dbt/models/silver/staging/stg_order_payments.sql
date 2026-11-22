
{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = '(order_id, payment_sequential)'
    )
}}

SELECT
    assumeNotNull(nullIf(trimBoth(toString(order_id)), ''))
        AS order_id,

    assumeNotNull(
        toUInt32OrNull(
            nullIf(trimBoth(toString(payment_sequential)), '')
        )
     ) AS payment_sequential,

    lowerUTF8(
        nullIf(trimBoth(toString(payment_type)), '')
    ) AS payment_type,

    toUInt32OrNull(
        nullIf(trimBoth(toString(payment_installments)), '')
    ) AS payment_installments,

    toFloat64OrNull(
        nullIf(trimBoth(toString(payment_value)), '')
    ) AS payment_value

FROM {{ source('olist_bronze', 'bronze_order_payments') }}

WHERE
    nullIf(trimBoth(toString(order_id)), '') IS NOT NULL
    AND toUInt32OrNull(
        nullIf(trimBoth(toString(payment_sequential)), '')
    ) IS NOT NULL
