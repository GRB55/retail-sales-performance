from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

def extract_data(parent_folder:str, subfolder:str, file:str, sheet=0) -> pd.DataFrame:
    """Function to load the data file in a dataframe.

    Args:
        parent_folder (str): parent folder where the file data is stored, normally 'data'.
        subfolder (str): folder inside of the parent folder where the data is stored, 'raw' for raw data and 'processed' for the processed dataset
        file (str): data file
        sheet (int): sheet number to be loaded, if 0 then the first, 1 the second and so on... 

    Raises:
        ValueError: if no sheet is selected

    Returns:
        pd.DataFrame: dataset loaded in a dataframe
    """
    file_path = BASE_DIR / parent_folder / subfolder / file
    
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)
    elif file_path.suffix.lower() == ".xlsx":
        excel = pd.ExcelFile(file_path)
        if sheet is None:
            if len(excel) > 1:
                print("El archivo tiene varias hojas, seleccione una:")
                print(pd.ExcelFile(file_path).sheet_names)
                raise ValueError("Debe especificar la hoja con el parámetro 'sheet'")
        return pd.read_excel(file_path, sheet_name=sheet)
    else:
        return "Load a .csv or .xlsx file."