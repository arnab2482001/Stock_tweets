import numpy as np
import pandas as pd
import nselib
from nselib import capital_market
from datetime import datetime, timedelta


def download_data_for_date_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        try:
            formatted_date = current_date.strftime("%d-%m-%Y")
            df = capital_market.bhav_copy_with_delivery(formatted_date)

            df['DELIV_PER'] = pd.to_numeric(df['DELIV_PER'], errors='coerce')
            condition = (
                    (df['SERIES'] == 'EQ') &
                    (df['TURNOVER_LACS'] > 100) &
                    (df['DELIV_PER'] > 85.00) &
                    (~df['SYMBOL'].str.endswith(('BEES', 'ETF', 'NIFTY', 'GOLD')))
            )
            new_df = df[condition]

            file_path = f'/home/subhamde/Desktop/Final Year Project/Stock-Tweets/Data/{formatted_date}_data.csv'
            new_df.to_csv(file_path, index=False)
            print(f"CSV file saved successfully for {formatted_date} at: {file_path}")
        except Exception as e:
            print(f"Holiday: {current_date.strftime('%d-%m-%Y')}")
        current_date += timedelta(days=1)


start_date_str = input("Enter start date in DD-MM-YYYY format (e.g., 01-05-2024): ")
end_date_str = input("Enter end date in DD-MM-YYYY format (e.g., 07-05-2024): ")

start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

download_data_for_date_range(start_date, end_date)
