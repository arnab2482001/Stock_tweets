import pandas as pd


# Function to sort a CSV file based on a specific column and print the first 15 rows
def sort_csv_by_delivery_percentage(csv_file):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file, usecols=['SYMBOL', 'DELIV_PER'])

        # Sort the DataFrame by the 'DELIV_PER' column in descending order
        df_sorted = df.sort_values(by='DELIV_PER', ascending=False)

        # Check if the DataFrame has at least 15 rows
        if len(df_sorted) >= 15:
            # Print only the first 15 rows
            print(df_sorted.head(15))
        else:
            # Print all rows if there are fewer than 15 rows
            print(df_sorted)

        print('CSV file with selected columns and first 15 rows printed successfully!')

    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


csv_file = "/home/subhamde/Desktop/Final Year Project/Stock-Tweets/Data/05-04-2024_data.csv"
sort_csv_by_delivery_percentage(csv_file)
