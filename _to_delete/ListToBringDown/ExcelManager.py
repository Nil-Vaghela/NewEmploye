import pandas as pd
from datetime import datetime
import os

class ExcelManager:
    def __init__(self, location_name):
        self.base_path = os.path.join(os.getcwd(), "Database")
        self.file_path = os.path.join(self.base_path, f"{location_name}.xlsx")
        self.list_file_path = os.path.join(self.base_path, f"{location_name}_BringDown.xlsx")
        self.location_name = location_name

    def update_quantity(self, product_name, new_quantity):
        df = pd.read_excel(self.list_file_path)
        df.loc[df['ProductName'].str.lower() == product_name.lower(), 'Quantity'] = new_quantity
        df.to_excel(self.list_file_path, index=False)

    def delete_item(self, product_name):
        list_df = pd.read_excel(self.list_file_path)
        # Find the item to delete and its quantity in the "Bring Down" list
        item_row = list_df[list_df['ProductName'].str.lower() == product_name.lower()]
        
        if not item_row.empty:
            delete_quantity = item_row.iloc[0]['Quantity']
            
            # Remove the item from the "Bring Down" list
            list_df = list_df[list_df['ProductName'].str.lower() != product_name.lower()]
            list_df.to_excel(self.list_file_path, index=False)
            
            # Load the master database
            master_df = pd.read_excel(self.file_path)
            # Check if the item exists in the master database
            if product_name.lower() in master_df['ProductName'].str.lower().values:
                # Subtract the quantity and update the master database
                master_df.loc[master_df['ProductName'].str.lower() == product_name.lower(), 'Quantity'] -= delete_quantity
                # Ensure quantity does not go negative
                master_df['Quantity'] = master_df['Quantity'].clip(lower=0)
                master_df.to_excel(self.file_path, index=False)

    def log_stock_movement(self, product_name, quantity,LocationNames):
        log_path = os.path.join(self.base_path, f"{LocationNames}StockMovementLog.xlsx")
        if not os.path.exists(log_path):
            log_df = pd.DataFrame(columns=['ProductName', 'Quantity', 'Timestamp'])
        else:
            log_df = pd.read_excel(log_path)

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_df = pd.concat([log_df, pd.DataFrame([{'ProductName': product_name, 'Quantity': quantity, 'Timestamp': now}])], ignore_index=True)
        log_df.to_excel(log_path, index=False)
