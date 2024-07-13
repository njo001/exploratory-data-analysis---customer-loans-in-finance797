# State of loans
import pandas as pd
import matplotlib.pyplot as plt
#%%

def calculate_recovery_statistics(df):
    total_recoveries = df['recoveries'].sum()
    total_funded_amount_inv = df['funded_amount_inv'].sum()
    total_loan_amount = df['loan_amount'].sum()

    recovery_percentage_inv = round((total_recoveries / total_funded_amount_inv) * 100, 2)
    recovery_percentage_total = round((total_recoveries / total_loan_amount) * 100, 2)

    return {
        'Total Recoveries': round(total_recoveries, 2),
        'Total Funded Amount by Investors': round(total_funded_amount_inv, 2),
        'Recovery Percentage for Investors': recovery_percentage_inv,
        'Total Funded Amount': round(total_loan_amount, 2),
        'Recovery Percentage in Total': recovery_percentage_total
    }

def calculate_loss(df):
    charged_off_df = df[df['loan_status'] == 'Charged Off'].copy()  # Ensure we're working with a copy

    # Convert relevant columns to numeric
    charged_off_df['term'] = charged_off_df['term'].str.replace('months', '', regex=False).astype(float)
    charged_off_df['instalment'] = pd.to_numeric(charged_off_df['instalment'], errors='coerce')
    charged_off_df['total_payment'] = pd.to_numeric(charged_off_df['total_payment'], errors='coerce')

    percentage_charged_off = round((len(charged_off_df) / len(df)) * 100, 2)
    total_paid_before_charged_off = round(charged_off_df['total_payment'].sum(), 2)

    charged_off_df['revenues_expected'] = round(charged_off_df['instalment'] * charged_off_df['term'], 2)
    charged_off_df['lost_revenue'] = round(charged_off_df['revenues_expected'] - charged_off_df['total_payment'], 2)

    return {
        'Percentage of loans charged off (%)': percentage_charged_off,
        'Amount paid off before charged off (GBP)': total_paid_before_charged_off,
        'Expected revenues if not charged off (GBP)': round(charged_off_df['revenues_expected'].sum(), 2),
        'Total lost revenues (GBP)': round(charged_off_df['lost_revenue'].sum(), 2)
    }

def visualize_projected_loss(charged_off_df):
    charged_off_df = charged_off_df.copy()  # Ensure we're working with a copy
    charged_off_df['issue_date'] = pd.to_datetime(charged_off_df['issue_date'], errors='coerce')
    charged_off_df['last_payment_date'] = pd.to_datetime(charged_off_df['last_payment_date'], errors='coerce')

    charged_off_df.loc[:, 'days_diff'] = (charged_off_df['last_payment_date'] - charged_off_df['issue_date']).dt.days
    charged_off_df.loc[:, 'term_days'] = charged_off_df['term'] * 30
    charged_off_df.loc[:, 'term_remaining'] = charged_off_df['term_days'] - charged_off_df['days_diff']

    plt.figure(figsize=(10, 6))
    plt.scatter(charged_off_df['days_diff'], charged_off_df['lost_revenue'])
    plt.title('Projected Loss Over Remaining Term of Charged Off Loans')
    plt.xlabel('Days Since Issue Date')
    plt.ylabel('Lost Revenue (GBP)')
    plt.show()

def calculate_behind_on_payments(df):
    behind_df = df[df['loan_status'].str.contains('Late', case=False)].copy()  # Ensure we're working with a copy
    charged_df = df[df['loan_status'].str.contains('Charged Off', case=False)].copy()  # Ensure we're working with a copy

    total_loans = len(df)
    behind_loans = len(behind_df)
    charged_off = len(charged_df)

    percentage_behind = (behind_loans / total_loans) * 100
    percentage_if_charged_off = ((behind_loans + charged_off) / total_loans) * 100

    total_amount_behind = behind_df['loan_amount'].sum()

    # Ensure numeric types
    behind_df.loc[:, 'term'] = behind_df['term'].str.replace('months', '', regex=False).astype(float)
    behind_df.loc[:, 'instalment'] = pd.to_numeric(behind_df['instalment'], errors='coerce')
    behind_df.loc[:, 'total_payment'] = pd.to_numeric(behind_df['total_payment'], errors='coerce')

    behind_df.loc[:, 'revenues_expected'] = round(behind_df['instalment'] * behind_df['term'], 2)
    behind_df.loc[:, 'lost_revenue'] = round(behind_df['revenues_expected'] - behind_df['total_payment'], 2)

    return {
        'Percentage behind (%)': round(percentage_behind, 2),
        'Total lost if charged off (GBP)': round(behind_df['lost_revenue'].sum(), 2),
        'Percentage of late plus charged off of total loans': percentage_if_charged_off
    }

def visualize_payments_by_status(df_combined):
    plt.figure(figsize=(12, 6))
    df_combined.boxplot(column='total_payment', by=['grade', 'status'], grid=False, patch_artist=True)
    plt.title('Payments Made by Loan Grade and Status')
    plt.suptitle('')  # Suppress the automatic title to keep it clean
    plt.xlabel('Grade and Status')
    plt.ylabel('Payments Made')
    plt.tick_params(axis='x', rotation=45)
    plt.show()

    plt.figure(figsize=(12, 6))
    df_combined.boxplot(column='total_payment', by=['purpose', 'status'], grid=False, patch_artist=True)
    plt.title('Payments Made by Purpose and Status')
    plt.suptitle('')  # Suppress the automatic title to keep it clean
    plt.xlabel('Purpose and Status')
    plt.ylabel('Payments Made')
    plt.tick_params(axis='x', rotation=45)
    plt.show()

def main():
    df = load_data('loan_payments.csv')

    # Recovery Statistics
    recovery_summary = calculate_recovery_statistics(df)
    print("Recovery Statistics:")
    print(recovery_summary)

    # Loss Calculation
    loss_summary = calculate_loss(df)
    print("\nLoss Summary:")
    print(loss_summary)
    
    # Visualize Projected Loss
    charged_off_df = df[df['loan_status'] == 'Charged Off'].copy()  # Ensure we're working with a copy
    visualize_projected_loss(charged_off_df)

    # Behind on Payments
    behind_summary = calculate_behind_on_payments(df)
    print("\nBehind on Payments Summary:")
    print(behind_summary)

    # Visualize Payments by Status
    df_combined = pd.concat([
        df[df['loan_status'].str.contains('Charged Off', case=False)].assign(status='Charged Off'),
        df[df['loan_status'].str.contains('Late', case=False)].assign(status='Late')
    ]).copy()  # Ensure we're working with a copy
    visualize_payments_by_status(df_combined)

if __name__ == "__main__":
    main()

# %%
