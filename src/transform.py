# Data manipulation
import pandas as pd

try:
    def transform(df:pd.DataFrame):
        df = df[df["Description"].notna() &
            (df["Quantity"] > 0) &
            (df["Price"] > 0) &
            (~df["Invoice"].astype(str).str.contains("C"))]
        df = df.drop_duplicates()
        df["Customer ID"] = df["Customer ID"].fillna("Unknown")
        df["Customer ID"] = df["Customer ID"].astype(str)
        df = df[df["StockCode"].astype(str).str.match(r"^\d+$")]
        df_cancellations = df[df["Invoice"].astype(str).str.contains("C")]
        df_variant = df[df["StockCode"].astype(str).str.match(r"^\d+[A-Za-z]+$")]
        df_special = df[df["StockCode"].astype(str).str.match(r"[A-Za-z]")]
        
        return df
except Exception as e:
    print(f"Something happened in the transformation, {e} raised, check the function.")