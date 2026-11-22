
{{
    config(
        materialized = 'table',
        schema = 'olist_gold',
        engine = 'MergeTree()',
        order_by = 'date_day'
    )
}}

WITH
date_bounds AS (
    SELECT
        assumeNotNull(
            min(toDate(order_purchase_timestamp))
        ) AS min_date,

        assumeNotNull(
            max(toDate(order_purchase_timestamp))
        ) AS max_date

    FROM {{ ref('stg_orders') }}
    WHERE isNotNull(order_purchase_timestamp)
),

date_range AS (
    SELECT
        min_date,
        max_date,

        toUInt64(
            greatest(
                dateDiff('day', min_date, max_date) + 1,
                toInt64(0)
            )
        ) AS total_days

    FROM date_bounds
)

SELECT
    addDays(min_date, number) AS date_day,

    toYear(date_day) AS year,
    toQuarter(date_day) AS quarter,
    toMonth(date_day) AS month,
    monthName(date_day) AS month_name,

    toDayOfMonth(date_day) AS day_of_month,
    toDayOfWeek(date_day) AS day_of_week,

    multiIf(
        toDayOfWeek(date_day) = 1, 'Monday',
        toDayOfWeek(date_day) = 2, 'Tuesday',
        toDayOfWeek(date_day) = 3, 'Wednesday',
        toDayOfWeek(date_day) = 4, 'Thursday',
        toDayOfWeek(date_day) = 5, 'Friday',
        toDayOfWeek(date_day) = 6, 'Saturday',
        'Sunday'
    ) AS day_name,

    if(
        toDayOfWeek(date_day) IN (6, 7),
        1,
        0
    ) AS is_weekend

FROM date_range
ARRAY JOIN range(total_days) AS number
