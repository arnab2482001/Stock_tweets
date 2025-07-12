import numpy as np
import pandas as pd
import nselib
from nselib import capital_market

# Get user input for date
date_input = input("Enter the date in DD-MM-YYYY format (e.g., 01-05-2024): ")

try:
    # Fetch Bhav Copy data for the specified date
    df = capital_market.bhav_copy_with_delivery(date_input)

    # Apply conditions to filter the dataframe
    df['DELIV_PER'] = pd.to_numeric(df['DELIV_PER'], errors='coerce')
    condition = (
            (df['SERIES'] == 'EQ') &
            (df['TURNOVER_LACS'] > 100) &
            (df['DELIV_PER'] > 85.00) &
            (~df['SYMBOL'].str.endswith(('BEES', 'ETF', 'NIFTY', 'GOLD')))
    ) # Add more conditions as needed
    new_df = df[condition]

    # Display the first few rows and columns of the dataframe
    print(new_df.head())
    print(df.columns.to_list())

    # Save filtered dataframe to CSV
    output_path = '/home/subhamde/Desktop/Final Year Project/Stock-Tweets/Data/after_sort.csv'
    new_df.to_csv(output_path, index=False)
    print(f"CSV file saved successfully at: {output_path}")
except Exception as e:
    print(e), print("Error in fetching Bhav Copy data")
