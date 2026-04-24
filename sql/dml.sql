/*
Sales by month
*/
SELECT
    dd.month_name,
    SUM(fs.total_amount) AS Total_sales
FROM
    fact_sales fs
JOIN
    dim_date dd
ON
    fs.date_id = dd.date_id
GROUP BY
    dd.month_name
ORDER BY
    Total_sales DESC;
/*
Sales by year
*/
SELECT
    dd.year,
    SUM(fs.total_amount) AS Total_sales
FROM
    fact_sales fs
JOIN
    dim_date dd
ON
    fs.date_id = dd.date_id
GROUP BY
    dd.year
ORDER BY
    Total_sales DESC;
/*
Average ticket
*/
SELECT
    invoice           AS Invoice,
    AVG(total_amount) AS avg_price
FROM
    fact_sales
WHERE
    invoice NOT LIKE 'C%'
GROUP BY
    invoice
ORDER BY
    invoice;
/*
Orders and units sold
*/
SELECT
    dd.year                    AS Year        ,
    dd.quarter                 AS Quarter     ,
    COUNT(DISTINCT fs.invoice) AS Total_orders,
    SUM(fs.quantity)           AS Units_sold
FROM
    fact_sales fs
JOIN
    dim_date dd
ON
    fs.date_id = dd.date_id
GROUP BY
    dd.year,
    dd.quarter
ORDER BY
    dd.year,
    dd.quarter;
/*
YoY variation
*/
WITH yearly_sales AS
     (
         SELECT
             dd.year              AS Year,
             SUM(fs.total_amount) AS Total_sales
         FROM
             fact_sales fs
         JOIN
             dim_date dd
         ON
             fs.date_id = dd.date_id
         GROUP BY
             dd.year )
SELECT
    Year        AS Actual_year ,
    Total_sales AS Actual_sales,
    LAG(Total_sales) OVER
        (
            ORDER BY
                Year
        )
    AS Past_sales              ,
    ((Total_sales - LAG(Total_sales) OVER
        (
            ORDER BY
                Year
        )
    ) / LAG(Total_sales) OVER
        (
            ORDER BY
                Year
        )
    ) * 100     AS YoY_pct
FROM
    yearly_sales;
/*
Monthly clients
*/
SELECT
    dd.month_name,
    COUNT(DISTINCT fs.customer_id) AS Unique_clients
FROM
    fact_sales fs
JOIN
    dim_date dd
ON
    fs.date_id = dd.date_id
GROUP BY
    dd.month_name
ORDER BY
    Unique_clients DESC;
/*
Top 10 clients
*/
SELECT TOP 10 customer_id AS Customer,
    SUM(total_amount)     AS Total_sales
FROM
    fact_sales
WHERE
    customer_id <> -1
GROUP BY
    customer_id
ORDER BY
    Total_sales DESC;
/*
RFM Analysis
*/
WITH customer_cte AS
     (
         SELECT
             fs.customer_id                           ,
             COUNT(DISTINCT fs.invoice) AS orders     ,
             SUM(fs.total_amount)       AS order_value,
             MAX(dd.full_date)          AS last_order_date
         FROM
             fact_sales fs
         JOIN
             dim_date dd
         ON
             fs.date_id = dd.date_id
         GROUP BY
             fs.customer_id )
SELECT
    *                ,
    ROUND(PERCENT_RANK() OVER
        (
            ORDER BY
                last_order_date
        )
    , 2) AS recency  ,
    ROUND(PERCENT_RANK() OVER
        (
            ORDER BY
                orders
        )
    , 2) AS frequency,
    ROUND(PERCENT_RANK() OVER
        (
            ORDER BY
                order_value
        )
    , 2) AS monetary
FROM
    customer_cte
ORDER BY
    last_order_date DESC;
/*
Retention rate between first and second year
*/
WITH year1_customers AS
     (
         SELECT DISTINCT
             fs.customer_id
         FROM
             fact_sales fs
         JOIN
             dim_date dd
         ON
             fs.date_id = dd.date_id
         WHERE
             dd.year        = 2010
         AND fs.customer_id <> -1 ),
     year2_customers AS
     (
         SELECT DISTINCT
             fs.customer_id
         FROM
             fact_sales fs
         JOIN
             dim_date dd
         ON
             fs.date_id = dd.date_id
         WHERE
             dd.year        = 2011
         AND fs.customer_id <> -1 )
SELECT
    COUNT(DISTINCT y1.customer_id)                                                    AS Customers_y1      ,
    COUNT(DISTINCT y2.customer_id)                                                    AS Retained_customers,
    ROUND(COUNT(DISTINCT y2.customer_id) * 100.0 / COUNT(DISTINCT y1.customer_id), 2) AS Retention_rate
FROM
    year1_customers y1
LEFT JOIN
    year2_customers y2
ON
    y1.customer_id = y2.customer_id;
/*
Top 20 most sold products
*/
SELECT TOP 20 fs.product_id         ,
    pd.description                  ,
    SUM(total_amount) AS Total_sales,
    SUM(quantity)     AS Units_sold
FROM
    fact_sales fs
JOIN
    dim_product pd
ON
    fs.product_id = pd.product_id
GROUP BY
    fs.product_id,
    pd.description
ORDER BY
    Total_sales DESC,
    Units_sold DESC;
/*
Most returned products
*/
SELECT
    product_id,
    (SUM(
        CASE
            WHEN
                quantity < 0
            THEN -quantity
            ELSE 0
        END) * 1.0 / NULLIF(SUM(
        CASE
            WHEN
                quantity > 0
            THEN quantity
            ELSE 0
        END), 0)) * 100 AS Return_rate
FROM
    fact_sales
GROUP BY
    product_id
ORDER BY
    Return_rate DESC;
/*
Products with most contributions to revenue
*/
WITH total_revenue AS
     (
         SELECT
             SUM(total_amount) AS total
         FROM
             fact_sales )
SELECT
    pd.description                          AS Product,
    (SUM(fs.total_amount) / tr.total) * 100 AS Contribution_revenue
FROM
    fact_sales fs
JOIN
    dim_product pd
ON
    fs.product_id = pd.product_id
CROSS JOIN
    total_revenue tr
GROUP BY
    pd.description,
    tr.total
ORDER BY
    Contribution_revenue DESC;
/*
Income by country
*/
SELECT
    dc.country           AS Country,
    SUM(fs.total_amount) AS Total_sales
FROM
    fact_sales fs
JOIN
    dim_customer cus
ON
    fs.customer_id = cus.customer_id
JOIN
    dim_country dc
ON
    cus.country_id = dc.country_id
GROUP BY
    dc.country
ORDER BY
    Total_sales DESC;
/*
Unique customers by country
*/
SELECT
    dc.country                     AS Country,
    COUNT(DISTINCT fs.customer_id) AS Unique_customer
FROM
    fact_sales fs
JOIN
    dim_customer cus
ON
    fs.customer_id = cus.customer_id
JOIN
    dim_country dc
ON
    cus.country_id = dc.country_id
GROUP BY
    dc.country
ORDER BY
    Unique_customer DESC;
/*
UK vs Rest of the World
*/
WITH uk_sales_cte AS
     (
         SELECT
             dc.country           AS Country,
             SUM(fs.total_amount) AS Uk_sales
         FROM
             fact_sales fs
         JOIN
             dim_customer cus
         ON
             fs.customer_id = cus.customer_id
         JOIN
             dim_country dc
         ON
             cus.country_id = dc.country_id
         WHERE
             dc.country = 'United Kingdom'
         GROUP BY
             dc.country)
SELECT
    uk.Uk_sales,
    SUM(fs.total_amount) AS Rest_world_sales
FROM
    fact_sales fs
JOIN
    dim_customer cus
ON
    fs.customer_id = cus.customer_id
JOIN
    dim_country dc
ON
    cus.country_id = dc.country_id
CROSS JOIN
    uk_sales_cte uk
WHERE
    dc.country <> 'United Kingdom'
GROUP BY
    uk.Uk_sales;
/*
Weekday sales
*/
SELECT
    dd.day_name          AS Weekday,
    SUM(fs.total_amount) AS Total_sales
FROM
    fact_sales fs
JOIN
    dim_date dd
ON
    fs.date_id = dd.date_id
GROUP BY
    dd.day_name
ORDER BY
    Total_sales DESC;