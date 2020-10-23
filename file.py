import pandas as pd
import numpy as np

# Read the csv from input folder.
df_ = pd.read_csv("./input/main.csv")
# Only rows that contain the country USA
df = df_[df_['COUNTRY'].str.contains("USA")].copy(deep=False)

df.to_csv('./output/filteredCountry.csv')
df = pd.read_csv("./output/filteredCountry.csv")

# Group by SKU
grouped = df.groupby('SKU')
# Replace extra signs from price
df['PRICE'] = df['PRICE'].str.replace('$', '').str.replace(',', '')
# Convert data type of column
df["PRICE"] = df["PRICE"].apply(pd.to_numeric,  errors='coerce')
# Fill empty space with NaN
df["PRICE"].replace('', np.nan, inplace=True)
# Drop the NaN
df = df.dropna()

# Find the minimum
dfMin = grouped['PRICE'].nsmallest(2)
# df2.to_csv('./output/check2.csv')
groupedMin = dfMin.groupby('SKU')
# Create list of rows to append data
rows = []
for name, group in groupedMin:
    ls = [name]
    for i in group:
        ls.append(i)
    rows.append(ls)

# Create the final dataframe
dfFin = pd.DataFrame(rows, columns=['SKU', 'FIRST_MINIMUM_PRICE', 'SECOND_MINIMUM_PRICE'])
dfFin.to_csv('./output/lowestPrice.csv', index=False)
