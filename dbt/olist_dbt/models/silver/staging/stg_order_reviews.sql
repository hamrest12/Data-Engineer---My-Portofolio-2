
{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = 'review_id'
    )
}}

SELECT
    assumeNotNull(nullIf(trimBoth(review_id), ''))
        AS review_id,

    nullIf(trimBoth(order_id), '') AS order_id,

    toUInt8OrNull(
        nullIf(trimBoth(review_score), '')
    ) AS review_score,

    nullIf(trimBoth(review_comment_title), '')
        AS review_comment_title,

    nullIf(trimBoth(review_comment_message), '')
        AS review_comment_message,

    parseDateTimeBestEffortOrNull(
        nullIf(trimBoth(review_creation_date), '')
    ) AS review_creation_date,

    parseDateTimeBestEffortOrNull(
        nullIf(trimBoth(review_answer_timestamp), '')
    ) AS review_answer_timestamp

FROM {{ source('olist_bronze', 'bronze_order_reviews') }}

WHERE
    nullIf(trimBoth(review_id), '') IS NOT NULL
