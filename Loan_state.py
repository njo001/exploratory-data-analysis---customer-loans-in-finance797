# State of loans

'''Summarise currently what percentage of the loans are recovered against the investor funding and the total amount funded. Visualise your results on an appropriate graph.

Additionally visualise what percentage of the total amount would be recovered up to 6 months' in the future.'''

import pandas as pd

df = pd.read_csv('loan_payments.csv')  

# Calculate the total recoveries
total_recoveries = df['recoveries'].sum()

# Calculate the total funded amount by investors
total_funded_amount_inv = df['funded_amount_inv'].sum()

# Calculate the total loan amount
total_loan_amount = df['loan_amount'].sum()

# Calculate the percentage of recoveries against the total funded amount by investors
recovery_percentage_inv = round((total_recoveries / total_funded_amount_inv) * 100,2)

# Calculate the percentage of recoveries against the total funded amount
recovery_percentage_total = round((total_recoveries / total_loan_amount) * 100,2)


# Summarize the results
summary = {
    'Total Recoveries': round(total_recoveries,2),
    'Total Funded Amount by Investors': round(total_funded_amount_inv,2),
    'Recovery Percentage for investors': recovery_percentage_inv,
    'Total Funded Amount': round(total_loan_amount,2),
    'Recovery Percentage in Total': recovery_percentage_total

}

summary

## Loss
'''Calculate the percentage of charged off loans historically and the total amount that was paid towards these loans before being charged off.'''

# Filter by charged off loans from loan_status
filtered_data = df[df['loan_status'] == 'Charged Off']

# Calculate percentage of charged off loans
percentage_charged_off = round((len(df[df['loan_status'] == 'Charged Off'])/ len(df['loan_status']))*100,2)
print('Percentage of loans charged off (%):', percentage_charged_off)

# Calculate total amounts payed towards charged off loans
total_payed_befor_charged_off = round(filtered_data['total_payment'].sum(),2)
print('Amount payed off before charged off (GBP):', total_payed_befor_charged_off)

loss_summary = {
    'Percentage of loans charged off (%)': percentage_charged_off,
    'Amount payed off before charged off (GBP)': total_payed_befor_charged_off

}

loss_summary

## Calculating projected loss
'''Calculate the projected loss of the loans marked as Charged Off.

Calculate the loss in revenue these loans would have generated for the company if they had finished their term. 
Visualise the loss projected over the remaining term of these loans.'''

# Calculate the loss in revenue
filtered_data.columns
filtered_data = filtered_data.dropna(subset=['term'])
filtered_data['term'] = filtered_data['term'].str.replace('months', '').str.strip().astype(int)

filtered_data['revenues_expected'] = round(filtered_data['instalment']*filtered_data['term'],2)
agg_revenues_expected = round(filtered_data['revenues_expected'].sum(),2)                                        
print("Expected revenues (GBP):", agg_revenues_expected)

filtered_data['lost_revenue'] = round(filtered_data['revenues_expected'] - filtered_data['total_payment'],2)
agg_lost_revenue = round(filtered_data['lost_revenue'].sum(),2)
print("Total lost revenues (GBP):", agg_lost_revenue) 

lost_revenue_summary = {
    "Expected revenues if not charged off (GBP)": agg_revenues_expected, 
    "Total lost revenues (GBP)": agg_lost_revenue
}

lost_revenue_summary

# Visulise loss projected


