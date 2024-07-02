# data_transform.py

import pandas as pd
import numpy as np

import pandas as pd

class DataTransform:
    def __init__(self, df):
        self.df = df
    
    
    def to_datetime(self, *cols, format=None):
        """
        Convert specified columns to datetime types.
        
        :param cols: Column names to convert.
        :param format: Optional date format for parsing. If None, will infer format.
        """
        for col in cols:
            self.df[col] = pd.to_datetime(self.df[col], format=format, errors='coerce')
        return self.df
    
    def to_categorical(self, *cols):
        """
        Convert specified columns to categorical types.
        
        :param cols: Column names to convert.
        """
        for col in cols:
            self.df[col] = self.df[col].astype('category')
        return self.df
    
 




 
