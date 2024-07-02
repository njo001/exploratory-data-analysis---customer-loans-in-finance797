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
        """Extract statistical values: median, standard deviation, and mean from numeric columns."""
          # Filter out categorical columns
        numeric_df = self.df.select_dtypes(include=[float, int])
        stats = {
            'median': numeric_df.median(),
            'std_dev': numeric_df.std(),
            'mean': numeric_df.mean()
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

    def check_duplicates(self):
        """Check for duplicate rows in the DataFrame."""
        duplicate_count = self.df.duplicated().sum()
        print(f"Number of duplicate rows: {duplicate_count}")
        return duplicate_count

    def count_values(self):
        """Count values in each column."""
        counts = {col: self.df[col].value_counts() for col in self.df.columns}
        return counts

    def correlation_matrix(self):
        """Generate and return the correlation matrix for numeric columns."""
        corr_matrix = self.df.corr()
        print("Correlation Matrix:")
        print(corr_matrix)
        return corr_matrix

# %%
