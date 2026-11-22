
{{
    config(
        materialized = 'table',
        schema = 'olist_gold',
        engine = 'MergeTree()',
        order_by = 'review_id'
    )
}}

SELECT
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date,
    review_answer_timestamp

FROM {{ ref('stg_order_reviews') }}
