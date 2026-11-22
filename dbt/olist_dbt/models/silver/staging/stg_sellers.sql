
{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = 'seller_id'
    )
}}

SELECT
    assumeNotNull(nullIf(trimBoth(seller_id), ''))
        AS seller_id,

    toUInt32OrNull(
        nullIf(trimBoth(seller_zip_code_prefix), '')
    ) AS seller_zip_code_prefix,

    lowerUTF8(
        nullIf(trimBoth(seller_city), '')
    ) AS seller_city,

    upperUTF8(
        nullIf(trimBoth(seller_state), '')
    ) AS seller_state

FROM {{ source('olist_bronze', 'bronze_sellers') }}

WHERE
    nullIf(trimBoth(seller_id), '') IS NOT NULL
