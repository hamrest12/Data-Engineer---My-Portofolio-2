
{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = 'geolocation_zip_code_prefix'
    )
}}

SELECT
    assumeNotNull(
        toUInt32OrNull(
            nullIf(trimBoth(toString(geolocation_zip_code_prefix)), '')
        )
    ) AS geolocation_zip_code_prefix,

    toFloat64OrNull(
        nullIf(trimBoth(toString(geolocation_lat)), '')
    ) AS geolocation_lat,

    toFloat64OrNull(
        nullIf(trimBoth(toString(geolocation_lng)), '')
    ) AS geolocation_lng,

    lowerUTF8(
        nullIf(trimBoth(toString(geolocation_city)), '')
    ) AS geolocation_city,

    upperUTF8(
        nullIf(trimBoth(toString(geolocation_state)), '')
    ) AS geolocation_state

FROM {{ source('olist_bronze', 'bronze_geolocation') }}

WHERE
    toUInt32OrNull(
        nullIf(trimBoth(toString(geolocation_zip_code_prefix)), '')
    ) IS NOT NULL
