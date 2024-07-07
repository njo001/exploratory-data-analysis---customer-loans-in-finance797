import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

class DataFrameTransform:
    def __init__(self, df):
        self.df = df

    def null_value_summary(self):
        """Generate a count/percentage count of NULL values in each column."""
        null_counts = self.df.isnull().sum()
        null_percentage = (null_counts / len(self.df)) * 100
        summary = pd.DataFrame({'Null Count': null_counts, 'Percentage': null_percentage})

        # Create index lists for cols to drop (NA > 50%) and cols to impute (NA >0 & < 50%)
        drop_columns = summary[summary['Percentage'] > 50].index.tolist()
        impute_columns = summary[(summary['Percentage'] > 0) & (summary['Percentage'] <= 50)].index.tolist()

        # Drop >50% null
        self.df.drop(columns=drop_columns, inplace=True)

        # Impute
        numeric_impute_columns = self.df[impute_columns].select_dtypes(include='number').columns.tolist()
        self.df[numeric_impute_columns] = self.df[numeric_impute_columns].fillna(self.df[numeric_impute_columns].mean())
        return summary, drop_columns, impute_columns, self.df

    def skewed_data(self):
        numeric_columns = self.df.select_dtypes(include='number').columns.tolist()
        for col in numeric_columns:
            self.df[col].hist(bins=50)
            plt.title(f'Histogram of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.show()
            print(f"Skew of {col} column is {self.df[col].skew()}")

    def log_transform_skewed_columns(self, skew_threshold=0.5):
        """Apply log transformation to columns with skewness above a certain threshold."""
        numeric_columns = self.df.select_dtypes(include='number').columns.tolist()
        skewed_columns = [col for col in numeric_columns if self.df[col].skew() > skew_threshold]

        for col in skewed_columns:
            # Apply log transformation directly
            self.df[col] = np.log(self.df[col])
            print(f"Applied log transformation to {col}")

    def remove_highly_correlated_columns(self, correlation_threshold=0.9):
        """Remove columns that are highly correlated (r > correlation_threshold)."""
        corr_matrix = self.df.corr().abs()
        upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        
        to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > correlation_threshold)]
        self.df.drop(columns=to_drop, inplace=True)
        
        return to_drop, self.df

class Plotter:
    def __init__(self, df):
        self.df = df

    def plot_null_percentage(self):
        """Plot the percentage of NULL values in each column as a bar plot."""
        null_counts = self.df.isnull().sum()
        null_percentage = (null_counts / len(self.df)) * 100
        summary = pd.DataFrame({'Percentage': null_percentage}).round(2)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(summary.index, summary['Percentage'])
        plt.xlabel('Columns')
        plt.ylabel('Percentage of NULL Values')
        plt.title('Percentage of NULL Values per Column')
        plt.xticks(rotation=45)
        plt.ylim(0, 100)
        plt.show()

    def plot_boxplots_with_outliers(self):
        """Plot boxplots and identify outliers for numeric columns."""
        numeric_columns = self.df.select_dtypes(include='number').columns.tolist()

        for col in numeric_columns:
            plt.figure(figsize=(8, 6))
            plt.boxplot(self.df[col], vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue'))

            # Identify outliers using 3 sd from mean
            m = self.df[col].mean()
            sd = self.df[col].std()
            lower_bound = m - sd * 3
            upper_bound = m + sd * 3
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col]

            # Plot outliers in red
            for outlier in outliers:
                plt.scatter(outlier, 1, color='red')

            plt.title(f'Boxplot of {col}')
            plt.xlabel(col)
            plt.show()

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('loan_payments.csv')

    # Instantiate the class
    transformer = DataFrameTransform(df)
    summary, drop_columns, impute_columns, transformed_df = transformer.null_value_summary()

    print("Null Value Summary:")
    print(summary)
    print("\nColumns to Drop:")
    print(drop_columns)
    print("\nColumns to Impute:")
    print(impute_columns)
    print("\nTransformed DataFrame:")
    print(transformed_df)

    plotter = Plotter(transformed_df)
    plotter.plot_null_percentage()
    plotter.plot_boxplots_with_outliers()

    analyser = DataFrameTransform(transformed_df)
    analyser.skewed_data()
    analyser.log_transform_skewed_columns(skew_threshold=0.5)

    to_drop, transformed_df = transformer.remove_highly_correlated_columns(correlation_threshold=0.9)
    print(f"Highly correlated columns removed: {to_drop}")

    numeric_df = transformed_df.select_dtypes(include='number')
    fig = px.imshow(numeric_df.corr(), title="Correlation Heatmap of Loan Payments DataFrame")
    fig.show()
