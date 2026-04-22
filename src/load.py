from sqlalchemy import create_engine, inspect
import pandas as pd

# Server where the database is stored
SERVER = "localhost\MSSQLSERVER2022"
# Database to be used
DATABASE = "OnlineRetail"

def load_data(df, SERVER, DATABASE):
    # Database connection
    connection_string = (
        f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    # Database management 
    engine = create_engine(connection_string, fast_executemany=True)
    
    with engine.begin() as conn:
    # Load data
        # Product dimension
        dim_product = (
            df[["stock_code", "product_base_code", "description", "is_variant"]].drop_duplicates(subset=["stock_code"]).reset_index(drop=True)
        )
        dim_product.to_sql("dim_product", con=conn, if_exists="append", index=False)
        # IDs
        product_map = pd.read_sql("SELECT product_id, stock_code FROM dim_product", conn)
        # Country dimension
        dim_country = (
            df[["country", "region"]].drop_duplicates(subset=["country"]).reset_index(drop=True)
        )
        dim_country.to_sql("dim_country", con=conn, if_exists="append", index=False)
        # IDs 
        country_map = pd.read_sql("SELECT country_id, country FROM dim_country", conn)
        # Customer dimension
        dim_customer = (
            df[["customer_id", "country"]]
        )
        dim_customer.to_sql("dim_customer", con=conn, if_exists="append", index=False)
        # Date dimension
        dim_date = (
            df[["full_date", "year", "quarter", "month", "month_name", "week", "day", "day_name", "is_weekend"]].drop_duplicates(subset=["full_date"])
        )
        dim_date.to_sql("dim_date", con=conn, if_exists="append", index=False)
        # IDs
        date_map = pd.read_sql("SELECT date_id, full_date FROM dim_date", conn)
        # Sales fact table development
        fact = df.copy()
        # Add the product_id
        fact = fact.merge(
            product_map,
            left_on="Stockcode", right_on="stock_code",
            how="left"
        )
        # Normalize the date to truncate the hours and minutes
        fact["full_date"] = pd.to_datetime(fact["InvoiceDate"]).dt.normalize()
        # Add the date_id
        fact = fact.merge(
            date_map,
            on="full_date",
            how="left"
        )
        fact_sales = (
            fact[["product_id", "customer_id", "date_id", "invoice", "quantity", "price", "total_amount", "is_return"]].reset_index(drop=True)
        )
        fact_sales.to_sql("fact_sales", con=conn, if_exists="append", index=False)
        
        print("=== LOAD COMPLETE ===")
        print(f"dim_product: {len(dim_product)} rows")
        print(f"dim_country: {len(dim_country)} rows")
        print(f"dim_customer: {len(dim_customer)} rows")
        print(f"dim_date: {len(dim_date)} rows")
        print(f"fact_sales: {len(fact_sales)} rows")