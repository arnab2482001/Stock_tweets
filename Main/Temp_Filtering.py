import numpy as np
import pandas as pd
import nselib
from nselib import capital_market

nselib.trading_holiday_calendar()
#date = input("Enter the date in format dd-mm-yyyy : ")
df = capital_market.bhav_copy_with_delivery("01-05-2024")
df.head()
df.columns.to_list()

condition = (df['SERIES'] == 'EQ') & (df['TURNOVER_LACS'] > 100) #& (df['DELIV_PER'] > 85.00)
new_df = df[condition]
# print(new_df)
new_df.to_csv('/home/subhamde/Desktop/Final Year Project/Stock-Tweets/Data/after_sort.csv', index=False)
print("CSV file saved successfully at : /Data")
