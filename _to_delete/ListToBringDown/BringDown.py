import pandas as pd
import os
from flask import Flask,render_template
from datetime import datetime
from Addstocks import Add_Stocks

class ListtobringDown:
    def MakeNewExcelFile(ProductName, Quantity,Locationname):
        Full_Path = os.path.join(os.getcwd(), "Database")
        FilePath = os.path.join(Full_Path, f"{Locationname}.xlsx")
        df = pd.read_excel(FilePath)

        List_FilePath = os.path.join(Full_Path, f"{Locationname}_BringDown.xlsx")
        List_df = pd.read_excel(List_FilePath)
        
        #Find Row with product name
        
        ProductRow = df[df["ProductName"].str.lower() == ProductName.lower()]
        if ProductRow.empty == True:
            return "Product Not Found"

        ProductDetails = ProductRow.to_dict(orient="records")[0]
        ProductDetails["Quantity"] = Quantity
        List_df = pd.concat([List_df, pd.DataFrame([ProductDetails])], ignore_index=True)
        List_df.to_excel(List_FilePath,index = False)

        ColumnList = Add_Stocks.AddProudctsPage.Fetchstocks(Locationname)
        
        StockRoomData = {col: [] for col in ColumnList }

        for _, row in List_df.iterrows():
            for stockroom in StockRoomData.keys():
                if row[stockroom] == 'Y':
                    # Append the row (as a dict) to the list of items for this stockroom
                    StockRoomData[stockroom].append(row.to_dict())
        return StockRoomData
    
    def ReadWorkingFile(LocationNme):
        Full_Path = os.path.join(os.getcwd(), "Database")
        FilePath = os.path.join(Full_Path, f"{LocationNme}.xlsx")
        df = pd.read_excel(FilePath)

        List_FilePath = os.path.join(Full_Path, f"{LocationNme}_BringDown.xlsx")
        List_df = pd.read_excel(List_FilePath)
        ColumnList = Add_Stocks.AddProudctsPage.Fetchstocks(LocationNme)
        
        StockRoomData = {col: [] for col in ColumnList }
        for _, row in List_df.iterrows():
            for stockroom in StockRoomData.keys():
                if row[stockroom] == 'Y':
                    # Append the row (as a dict) to the list of items for this stockroom
                    StockRoomData[stockroom].append(row.to_dict())
        return StockRoomData
    
    def ItemLists(LocationName):
        Full_Path = os.path.join(os.getcwd(), "Database")
        FilePath = os.path.join(Full_Path, f"{LocationName}.xlsx")
        df = pd.read_excel(FilePath)
        if os.path.exists(FilePath):
            df = pd.read_excel(FilePath)
            item_names = df['ProductName'].unique().tolist()
        else:
            item_names = []
        
        return item_names

