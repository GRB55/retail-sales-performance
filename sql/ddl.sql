CREATE DATABASE OnlineRetail;
USE OnlineRetail;
CREATE TABLE dim_product
    (
        product_id        INT IDENTITY PRIMARY KEY,
        stockcode         NVARCHAR(10) NOT NULL   ,
        product_base_code INT NOT NULL            ,
        description       NVARCHAR(256) NOT NULL  ,
        has_variants      BIT NULL
    )
;
CREATE TABLE dim_country
    (
        country_id INT IDENTITY PRIMARY KEY,
        country    VARCHAR(32) NOT NULL    ,
        region     VARCHAR(32) NOT NULL
    )
;
CREATE TABLE dim_customer
    (
        customer_id INT PRIMARY KEY,
        country_id  INT FOREIGN KEY REFERENCES dim_country(country_id)
    )
;
CREATE TABLE dim_date
    (
        date_id    INT IDENTITY PRIMARY KEY,
        full_date  DATE NOT NULL           ,
        year       INT NOT NULL            ,
        quarter    TINYINT NOT NULL        ,
        month      INT NOT NULL            ,
        month_name VARCHAR(16) NOT NULL    ,
        week       INT NOT NULL            ,
        day        INT NOT NULL            ,
        day_name   VARCHAR(16) NOT NULL    ,
        is_weekend BIT NOT NULL
    )
;
CREATE TABLE fact_sales
    (
        sales_id     INT IDENTITY PRIMARY KEY                            ,
        product_id   INT FOREIGN KEY REFERENCES dim_product(product_id)  ,
        customer_id  INT FOREIGN KEY REFERENCES dim_customer(customer_id),
        date_id      INT FOREIGN KEY REFERENCES dim_date(date_id)        ,
        invoice      NVARCHAR(16) NOT NULL                               ,
        quantity     INT NOT NULL                                        ,
        unit_price   DECIMAL(10, 2) NOT NULL                             ,
        total_amount DECIMAL(10, 2) NOT NULL                             ,
        is_return    BIT NOT NULL DEFAULT = 0
    );