
SELECT
    orders.order_id,
    orders.customer_id

FROM {{ ref('fct_orders') }} AS orders

LEFT JOIN {{ ref('dim_customers') }} AS customers
    ON orders.customer_id = customers.customer_id

WHERE customers.customer_id IS NULL
