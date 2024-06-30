import yaml
from sqlalchemy import create_engine
import pandas as pd

# Load credentials
def load_credentials(filename='credentials.yaml'):
    with open(filename, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

# RDS Database Connector class
class RDSDatabaseConnector:
    def __init__(self, credentials):
        self.host = credentials['RDS_HOST']
        self.password = credentials['RDS_PASSWORD']
        self.user = credentials['RDS_USER']
        self.database = credentials['RDS_DATABASE']
        self.port = credentials['RDS_PORT']
        self.engine = None

    def initialize_engine(self):
        connection_string = (
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )
        self.engine = create_engine(connection_string)

    def extract_data(self, query="SELECT * FROM loan_payments"):
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
    connector.initialize_engine()  # This should match the method name in your class
    data = connector.extract_data()
    save_data_to_csv(data)
