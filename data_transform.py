
# %%
import pandas as pd
import numpy as np
from datetime import datetime

class DataTransform:
    def __init__(self, df):
        self.df = df

    def convert_to_datetime(self):
        # Identify object type columns
        object_cols = self.df.select_dtypes(include=['object']).columns

        for col in object_cols:
            print(f"Checking column: {col}")
            if self.df[col].str.contains('-').any():
                print(f"Attempting to convert column {col} to datetime")
                try:
                    # Attempt to convert column to datetime
                    self.df[col] = pd.to_datetime(self.df[col], format='%b-%Y', errors='raise')
                    # Format the datetime to 'Month-Year'
                    self.df[col] = self.df[col].dt.strftime('%B-%Y')
                    print(f"Column {col} successfully converted to datetime")
                except ValueError as e:
                    # If conversion fails, print a message and continue
                    print(f"Column {col} does not contain month information or is not in the expected format. Error: {e}")
        
        return self.df

    def convert_to_category(self):
        # Identify remaining object type columns
        object_cols = self.df.select_dtypes(include=['object']).columns

        for col in object_cols:
            if not pd.api.types.is_datetime64_any_dtype(self.df[col]):
                print(f"Converting column {col} to category")
                self.df[col] = pd.Categorical(self.df[col])
        
        return self.df

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('loan_payments.csv')
   
    # Instantiate the class
    transformed_df = DataTransform(df)
    transformed_df.convert_to_datetime()
    transformed_df.convert_to_category()
    
    # Print the data types and the first few rows of the DataFrame
    print(transformed_df.df.dtypes)
    print(transformed_df.df.head())

   

