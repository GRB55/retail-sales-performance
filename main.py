from src.extract import extract_data
from src.transform import transform
from src.load import load_data
import pandas as pd

# Server where the database is stored
SERVER = "localhost\MSSQLSERVER2022"
# Database to be used
DATABASE = "OnlineRetail"

def main():
    df_2009_2010 = extract_data("data", "raw", "online_retail_ii.xlsx")
    df_2010_2011 = extract_data("data", "raw", "online_retail_ii.xlsx", sheet=1)
    df = pd.concat([df_2009_2010, df_2010_2011])
    df = transform(df)
    load_data(df, SERVER, DATABASE)
    
if __name__ == "__main__":
    main()