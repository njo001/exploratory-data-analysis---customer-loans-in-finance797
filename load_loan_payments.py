import pandas as pd

def load_data_from_csv(filename):
    """
    Load data from a CSV file into a Pandas DataFrame.
    
    Parameters:
    filename (str): The path to the CSV file.
    
    Returns:
    pd.DataFrame: DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(filename)


if __name__ == "__main__":
    # Load the data from a CSV file in the same directory
    df = load_data_from_csv('loan_payments.csv')
    
    # Print the first few rows of the DataFrame
    print(df.head())


