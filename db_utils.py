# db_utils.py

import psycopg2
import pandas as pd
from sqlalchemy import create_engine


class RDSDatabaseConnector:
    def __init__(self, credentials):
        """
        Initialize the RDSDatabaseConnector with database credentials.

        Parameters:
        credentials (dict): A dictionary containing database connection details.
        """
        # Initialize the class with credentials from the dictionary
        self.host = credentials['RDS_HOST']
        self.password = credentials['RDS_PASSWORD']
        self.user = credentials['RDS_USER']
        self.database = credentials['RDS_DATABASE']
        self.port = credentials['RDS_PORT']




def initialize_engine(self):
    ''' initilise engine connection'''
    connection_string = (
        f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )
    self.engine = create_engine(connection_string)

def extract_data(self, query="SELECT * FROM loan_payments"):
    ''' extract data using pandas'''

    if self.engine is not None:
        return pd.read_sql(query, self.engine)
    else:
        raise Exception("Engine not initialized")    
    
# Save data to CSV
def save_data_to_csv(dataframe, filename='loan_payments.csv'):
    dataframe.to_csv(filename, index=False)

# Main script
if __name__ == "__main__":
    credentials = load_credentials()
    connector = RDSDatabaseConnector(credentials)
    connector.initialize_engine()
    data = connector.extract_data()
    save_data_to_csv(data)    