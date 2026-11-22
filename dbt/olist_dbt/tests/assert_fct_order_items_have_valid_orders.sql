
SELECT
    items.order_id

FROM {{ ref('fct_order_items') }} AS items

LEFT JOIN {{ ref('fct_orders') }} AS orders
    ON items.order_id = orders.order_id

WHERE orders.order_id IS NULL
