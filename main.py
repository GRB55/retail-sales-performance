from src.extract import extract_data
from src.transform import transform
from src.load import load_data
import pandas as pd
from pathlib import Path

# Server where the database is stored
SERVER = r"localhost\MSSQLSERVER2022"
# Database to be used
DATABASE = "OnlineRetail"
# Base directory
BASE_DIR = Path(__file__).resolve().parent

def main():
    df_2009_2010 = extract_data(BASE_DIR, "data", "raw", "online_retail_ii.xlsx")
    df_2010_2011 = extract_data(BASE_DIR, "data", "raw", "online_retail_ii.xlsx", sheet=1)
    df = pd.concat([df_2009_2010, df_2010_2011], ignore_index=True)
    df = transform(df)
    load_data(df, SERVER, DATABASE)
    
if __name__ == "__main__":
    main()