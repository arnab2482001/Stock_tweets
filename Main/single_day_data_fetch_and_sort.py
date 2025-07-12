import numpy as np
import pandas as pd
from nselib import capital_market
from datetime import datetime

def is_weekend(date_input):
    return date_input.weekday() >= 5  # Saturday (5) and Sunday (6)

def fetch_and_sort_data(date_input):
    try:
        # Format the date
        formatted_date = date_input.strftime("%d-%m-%Y")

        # Fetch Bhav Copy data for the specified date
        df = capital_market.bhav_copy_with_delivery(formatted_date)

        # Convert 'DELIV_PER' column to numeric using NumPy
        df['DELIV_PER'] = pd.to_numeric(df['DELIV_PER'], errors='coerce')

        # Apply filtering conditions using vectorized operations
        condition = (
                (df['SERIES'] == 'EQ') &
                (df['TURNOVER_LACS'] > 100) &
                (df['DELIV_PER'] > 85.00) &
                (~df['SYMBOL'].str.endswith(('BEES', 'ETF', 'NIFTY', 'GOLD')))
        )
        filtered_df = df[condition]

        # Sort by DELIV_PER in descending order using NumPy
        sorted_indices = np.argsort(filtered_df['DELIV_PER'].values)[::-1]
        sorted_df = filtered_df.iloc[sorted_indices[:15]]  # Select top 15 rows

        # Create DataFrame with only the required columns
        result_df = pd.DataFrame({
            'SYMBOL': sorted_df['SYMBOL'].values,
            'DELIV_PER': sorted_df['DELIV_PER'].values
        })

        # Save the result to a CSV file with a custom name based on the date
        date_data = date_input.strftime("%Y-%m-%d")
        file_name = f"/home/subhamde/Desktop/Final Year Project/Stock-Tweets/Data/{date_data}_sorted_data.csv"
        result_df.to_csv(file_name, index=False)

        print(f"Data saved to '{file_name}' successfully!")

    except Exception as e:
        print("An error occurred:", e)


# Get user input for date
date_input_str = input("Enter the date in DD-MM-YYYY format (e.g., 01-05-2024): ")
date_input = datetime.strptime(date_input_str, "%d-%m-%Y")

# Call the function with user input date
fetch_and_sort_data(date_input)
