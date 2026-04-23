# Data manipulation
import pandas as pd


def transform(df:pd.DataFrame):
    try:
        print("=== BEFORE TRANSFORMATION ===")
        print(f"Quantity of rows: {df.shape[0]}")
        print(f"Quantity of columns: {df.shape[1]}")
        print(f"Total data: {df.size}")
        print(f"Duplicated values: {df.duplicated().sum()}")
        print(f"Null values: {df.isna().sum().sum()}")
        # Dictionary to map the region to the existing country
        country_region = {
        "United Kingdom": "Western Europe",
        "France": "Western Europe",
        "Belgium": "Western Europe",
        "Germany": "Western Europe",
        "Portugal": "Western Europe",
        "Netherlands": "Western Europe",
        "Spain": "Western Europe",
        "Italy": "Western Europe",
        "Austria": "Western Europe",
        "Switzerland": "Western Europe",
        "Ireland": "Western Europe",
        "Channel Islands": "Western Europe", 
        "Denmark": "Northern Europe",
        "Norway": "Northern Europe",
        "Sweden": "Northern Europe",
        "Finland": "Northern Europe",
        "Iceland": "Northern Europe",
        "Lithuania": "Northern Europe",
        "Cyprus": "Southern Europe",
        "Greece": "Southern Europe",
        "Malta": "Southern Europe",
        "Poland": "Eastern Europe",
        "Czech Republic": "Eastern Europe",
        "European Community" : "Western Europe",
        "United Arab Emirates": "Middle East",
        "Bahrain": "Middle East",
        "Israel": "Middle East",
        "Lebanon": "Middle East",
        "Saudi Arabia": "Middle East",
        "Japan": "East Asia",
        "Hong Kong": "East Asia",
        "Singapore": "East Asia",
        "Korea": "East Asia",
        "Thailand": "Southeast Asia",
        "Australia": "Oceania",
        "Nigeria": "Africa",
        "Republic of South Africa": "Africa",         
        "United States of America": "North America",
        "Canada": "North America",
        "Bermuda": "Caribbean",
        "West Indies": "Caribbean",
        "Brazil": "South America",
        "Unspecified": "Unknown"
        }
        # Filter data errors
        df_transformed = df[df["Description"].notna() & (~df["StockCode"].astype(str).str.match(r"[a-z-A-Z]"))].copy()
        # Drop duplicates
        df_transformed = df_transformed.drop_duplicates()
        # Map country aliases and create the region
        df_transformed["Country"] = df_transformed["Country"].str.replace("USA", "United States of America", regex=False)
        df_transformed["Country"] = df_transformed["Country"].str.replace("RSA", "Republic of South Africa", regex=False)
        df_transformed["Country"] = df_transformed["Country"].str.replace("EIRE", "Ireland", regex=False)
        df_transformed["region"] = df_transformed["Country"].map(country_region)
        # Fill customerid nulls with -1
        df_transformed["Customer ID"] = df_transformed["Customer ID"].fillna(-1)
        # Date data for the calendar table
        df_transformed["year"] = df_transformed["InvoiceDate"].dt.year
        df_transformed["quarter"] = df_transformed["InvoiceDate"].dt.quarter
        df_transformed["month"] = df_transformed["InvoiceDate"].dt.month
        df_transformed["month_name"] = df_transformed["InvoiceDate"].dt.month_name()
        df_transformed["week"] = df_transformed["InvoiceDate"].dt.strftime("%W") # Week of the year, starting Monday. If we want to start on Sunday we should use '%U'.
        df_transformed["day"] = df_transformed["InvoiceDate"].dt.day
        df_transformed["day_name"] = df_transformed["InvoiceDate"].dt.day_name()
        # Total amount
        df_transformed["total_amount"] = df_transformed["Quantity"] * df_transformed["Price"]
        # Product base code
        df_transformed["product_base_code"] = df_transformed["StockCode"].astype(str).str.extract(r"^(\d+)")
        # Flags
        df_transformed["is_weekend"] = df_transformed["InvoiceDate"].dt.day_of_week >= 5
        df_transformed["is_return"] = df_transformed["Invoice"].astype(str).str.startswith("C")
        df_transformed["has_variants"] = df_transformed["StockCode"].astype(str).str.match(r"^\d+[A-Za-z]+$")
        # Rename columns to match the database ones
        df_transformed.rename(columns={"Invoice": "invoice",
                           "StockCode": "stock_code",
                           "Description": "description",
                           "Quantity": "quantity",
                           "InvoiceDate": "full_date",
                           "Price": "unit_price",
                           "Customer ID": "customer_id",
                           "Country": "country"}, inplace=True)
        
        print("=== AFTER TRANSFORMATION ===")
        print(f"Quantity of rows: {df_transformed.shape[0]}")
        print(f"Quantity of columns: {df_transformed.shape[1]}")
        print(f"Total data: {df_transformed.size}")
        print(f"Duplicate values: {df_transformed.duplicated().sum()}")
        print(f"Null values: {df_transformed.isna().sum().sum()}")
        
        return df_transformed
    except Exception as e:
        print(f"Something happened in the transformation, {e} raised, check the function.")