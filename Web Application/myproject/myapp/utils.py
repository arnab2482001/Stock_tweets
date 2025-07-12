# myapp/utils.py
import numpy as np
import pandas as pd
from nselib import capital_market
from datetime import datetime, timedelta
import os


def is_weekend(date_input):
    return date_input.weekday() >= 5  # Saturday (5) and Sunday (6)


def fetch_and_sort_data(date_input):
    global formatted_date
    try:
        # Format the date
        formatted_date = date_input.strftime("%d-%m-%Y")

        # Fetch Bhav Copy data for the specified date
        df = capital_market.bhav_copy_with_delivery(formatted_date)

        # Debug print
        print(f"Data fetched for date: {formatted_date}")
        print(df.head())

        # Convert 'DELIV_PER' column to numeric using NumPy
        df["DELIV_PER"] = pd.to_numeric(df["DELIV_PER"], errors="coerce")

        # Apply filtering conditions using vectorized operations
        condition = (
            (df["SERIES"] == "EQ")
            & (df["TURNOVER_LACS"] > 100)
            & (df["DELIV_PER"] > 85.00)
            & (~df["SYMBOL"].str.endswith(("BEES", "ETF", "NIFTY", "GOLD")))
        )
        filtered_df = df[condition]

        # Sort by DELIV_PER in descending order using NumPy
        sorted_indices = np.argsort(filtered_df["DELIV_PER"].values)[::-1]
        sorted_df = filtered_df.iloc[sorted_indices[:15]]  # Select top 15 rows

        # Create DataFrame with only the required columns
        result_df = pd.DataFrame(
            {
                "SYMBOL": sorted_df["SYMBOL"].values,
                "DELIV_PER": sorted_df["DELIV_PER"].values,
            }
        )

        return result_df, None  # Return the sorted DataFrame

    except Exception as e:
        error_message = f"Error processing data for {formatted_date}: {e}"
        return (
            None,
            error_message,
        )  # Return None and the error message if there's an error


def process_data_range(start_date, end_date):
    try:
        # Convert start and end dates to datetime objects
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

        # Check if start date is before end date
        if start_date > end_date:
            return None, "Start date cannot be after end date"

        # Initialize dictionaries to store count and sum for each SYMBOL
        count_dict = {}
        sum_dict = {}

        # Loop through the date range and fetch data for each date
        date_range = pd.date_range(start=start_date, end=end_date)
        for date_input in date_range:
            if not is_weekend(date_input):
                df, error_message = fetch_and_sort_data(date_input)
                if df is not None:
                    # Debug print
                    print(f"Data for date {date_input}:")
                    print(df.head())

                    # Count 'SYMBOL' occurrences and calculate 'DELIV_PER' average
                    for symbol in df["SYMBOL"]:
                        count_dict[symbol] = count_dict.get(symbol, 0) + 1
                        sum_dict[symbol] = (
                            sum_dict.get(symbol, 0)
                            + df[df["SYMBOL"] == symbol]["DELIV_PER"].values[0]
                        )
                else:
                    return None, error_message

        # Create DataFrame for 'SYMBOL', 'TOTAL_COUNT', 'AVG_DELIV_PER'
        data = {
            "SYMBOL": list(count_dict.keys()),
            "TOTAL_COUNT": list(count_dict.values()),
            "AVG_DELIV_PER": [
                round(sum_dict[s] / count_dict[s], 2) for s in count_dict.keys()
            ],
        }
        result_df = pd.DataFrame(data)

        # Filter SYMBOLs with TOTAL_COUNT > 5 and Sort by 'TOTAL_COUNT' in descending order
        result_df = result_df[result_df["TOTAL_COUNT"] >= 5].sort_values(
            by="TOTAL_COUNT", ascending=False
        )

        # Save the result to a CSV file
        csv_path = os.path.join(
            "myapp/Data",
            f'symbol_stats({start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}).csv',
        )
        result_df.to_csv(csv_path, index=False)

        return (
            result_df,
            None,
            csv_path,
        )  # Return the final DataFrame, no error message, and the CSV path

    except ValueError as ve:
        return None, str(ve), None
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}", None
