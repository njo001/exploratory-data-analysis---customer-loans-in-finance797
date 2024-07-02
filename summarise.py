# Some useful utility methods you might want to create that are often used for EDA tasks are:

#Describe all columns in the DataFrame to check their data types
#Extract statistical values: median, standard deviation and mean from the columns and the DataFrame
#Count distinct values in categorical columns
#Print out the shape of the DataFrame
#Generate a count/percentage count of NULL values in each column
#Any other methods you may find useful

#%%
import pandas as pd

class DataFrameInfo:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def describe_columns(self):
        """Describe all columns in the DataFrame to check their data types and summary statistics."""
        print("Data Types:")
        print(self.df.dtypes)
        print("\nSummary Statistics:")
        print(self.df.describe(include='all'))

    def statistical_summary(self):
        """Extract statistical values: median, standard deviation, and mean from numeric columns only."""
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        stats = {
            'median': self.df[numeric_cols].median(),
            'std_dev': self.df[numeric_cols].std(),
            'mean': self.df[numeric_cols].mean()
        }
        return stats

    def count_distinct_values(self):
        """Count distinct values in categorical columns."""
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        distinct_counts = {col: self.df[col].nunique() for col in categorical_cols}
        return distinct_counts

    def print_shape(self):
        """Print out the shape of the DataFrame (number of rows and columns)."""
        print(f"DataFrame Shape: {self.df.shape}")

    def null_value_summary(self):
        """Generate a count/percentage count of NULL values in each column."""
        null_counts = self.df.isnull().sum()
        null_percentage = (null_counts / len(self.df)) * 100
        summary = pd.DataFrame({'Null Count': null_counts, 'Percentage': null_percentage})
        return summary



# %%

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('loan_payments.csv')
   
    # Instantiate the class
    df = DataFrameInfo(df)
    df.describe_columns()
    df.statistical_summary()
    df.count_distinct_values()

  
 