import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import pandas as pd
from nselib import capital_market
from datetime import datetime, timedelta
from pandasgui import show


def is_weekend(date_input):
    return date_input.weekday() >= 5  # Saturday (5) and Sunday (6)


def fetch_and_sort_data(date_input):
    global formatted_date
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
        # result_df = pd.DataFrame({
        #     'SYMBOL': sorted_df['SYMBOL'].values,
        #     'DELIV_PER': sorted_df['DELIV_PER'].values
        # })
        result_df = pd.DataFrame({
            'SYMBOL': sorted_df.loc[:, 'SYMBOL'].values,
            'DELIV_PER': sorted_df.loc[:, 'DELIV_PER'].values
        })
        return result_df  # Return the sorted DataFrame

    except Exception as e:
        print(f"Error processing data for {formatted_date}: {e}")
        return None  # Return None if there's an error


def process_data_range():
    start_date_str = start_date_entry.get()
    end_date_str = end_date_entry.get()

    try:
        # Convert start and end dates to datetime objects
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

        # Check if start date is before end date
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")

        # Initialize dictionaries to store count and sum for each SYMBOL
        count_dict = {}
        sum_dict = {}

        # Loop through the date range and fetch data for each date
        date_range = pd.date_range(start=start_date, end=end_date)
        for date_input in date_range:
            if not is_weekend(date_input):
                df = fetch_and_sort_data(date_input)
                if df is not None:
                    # Count 'SYMBOL' occurrences and calculate 'DELIV_PER' average
                    for symbol in df['SYMBOL']:
                        count_dict[symbol] = count_dict.get(symbol, 0) + 1
                        sum_dict[symbol] = sum_dict.get(symbol, 0) + df[df['SYMBOL'] == symbol]['DELIV_PER'].values[0]

        # Create DataFrame for 'SYMBOL', 'TOTAL_COUNT', 'AVG_DELIV_PER'
        data = {'SYMBOL': list(count_dict.keys()), 'TOTAL_COUNT': list(count_dict.values()),
                'AVG_DELIV_PER': [sum_dict[s] / count_dict[s] for s in count_dict.keys()]}
        result_df = pd.DataFrame(data)

        # Filter SYMBOLs with TOTAL_COUNT > 5 and Sort by 'TOTAL_COUNT' in descending order
        result_df = result_df[result_df['TOTAL_COUNT'] >= 5].sort_values(by='TOTAL_COUNT', ascending=False)

        # Save the result to a CSV file
        start = start_date.strftime("%Y-%m-%d")
        end = end_date.strftime("%Y-%m-%d")
        csv_file_path = f'/home/subhamde/Desktop/Final Year Project/Stock-Tweets/Data/symbol_stats({start} to {end}).csv'
        result_df.to_csv(csv_file_path, index=False)
        messagebox.showinfo("Success", f"Data saved successfully to {csv_file_path}")

        # Display CSV file in Excel format
        show(result_df.iloc[:, :])

        # Destroy the root window after processing
        root.destroy()

    except ValueError as ve:
        messagebox.showerror("Error", f"ValueError: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main window
root = tk.Tk()
root.title("Data Processing")

# Create labels and entry fields for user input
start_date_label = ttk.Label(root, text="Start Date (DD-MM-YYYY):")
start_date_label.pack()
start_date_entry = ttk.Entry(root)
start_date_entry.pack()

end_date_label = ttk.Label(root, text="End Date (DD-MM-YYYY):")
end_date_label.pack()
end_date_entry = ttk.Entry(root)
end_date_entry.pack()

# Create a button to trigger data processing
process_button = ttk.Button(root, text="Process Data", command=process_data_range)
process_button.pack()

# Run the main event loop
root.mainloop()
