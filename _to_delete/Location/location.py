# Every code related to Location page goes here
import pandas as pd
import os


class Location():
    def ShowLocation():
        Location_Files = []
        for i in os.listdir("Database"):
            if i.endswith('.xlsx'):
                Location_Files.append(i)
                if i.endswith("_BringDown.xlsx"):
                    Location_Files.remove(i)
                if i.endswith("MovementLog.xlsx"):
                    Location_Files.remove(i)
        return Location_Files
    
    def addLocation(Locationsname,Stockrooms):
        LocationName = Locationsname

        #These are user input for stockroom names
        
        NameOfStockRoom = Stockrooms
    
    # These are PreDefine Static column Names
        DefaultColumns = ["ProductName","Quantity"]
        CustomColumns = DefaultColumns + NameOfStockRoom #merged two List

    #GetPath To Save Excel File

        Full_Path = os.path.join(os.getcwd(),"Database")

        df = pd.DataFrame(columns=CustomColumns)

        FilePath = os.path.join(Full_Path,f"{LocationName}.xlsx") # Get Final Path
        ListToBringDownExcelFile = os.path.join(Full_Path,f"{LocationName}_BringDown.xlsx") # Get Final Path
        df.to_excel(FilePath,index=False,index_label="")
        df.to_excel(ListToBringDownExcelFile,index=False,index_label="")