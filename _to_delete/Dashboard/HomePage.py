import os
import pandas as pd


class homepageReports:
    def check_stock(LocationName, low_stock_threshold):
     Full_Path = os.path.join(os.getcwd(), "Database")
     FilePath = os.path.join(Full_Path, f"{LocationName}.xlsx")
     df = pd.read_excel(FilePath)
    # Assuming column names are 'ProductName' and 'Quantity'
     out_of_stock = df[df['Quantity'] == 0]['ProductName'].tolist()
     low_stock = df[(df['Quantity'] > 0) & (df['Quantity'] <= low_stock_threshold)]['ProductName'].tolist()

     return out_of_stock, low_stock

    def total_items(LocationName):
        Full_Path = os.path.join(os.getcwd(), "Database")
        FilePath = os.path.join(Full_Path, f"{LocationName}.xlsx")
        df = pd.read_excel(FilePath)
        return df['Quantity'].sum()
    
    