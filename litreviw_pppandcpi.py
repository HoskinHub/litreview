#ppp and cpi procressing

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#import cpi csv file
df = pd.read_csv('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_code/CPI USA PPP.csv', encoding='latin1')

#get median cpi per year
df['YEAR'] = df['DATE'].str[:4]
yearly_median = df.groupby('YEAR')['CPIAUCSL'].median()
df['MEDFORYEAR'] = df['YEAR'].map(yearly_median)

#calculate percent differences between CPIs
med_for_2024 = df[df['YEAR'] == '2024']['MEDFORYEAR'].iloc[0]
print(med_for_2024)

# Step 5: Transform the 'CPIAUCSL' values for each year relative to the 2024 CPI
df['FACTOR'] = (med_for_2024/ df['MEDFORYEAR'])

# Output the result
print(df[['DATE', 'CPIAUCSL', 'YEAR', 'MEDFORYEAR', 'FACTOR']])

# Print the column names of the DataFrame
print(df.columns)

#import my data collection Excel file using openpyxl
df1 = pd.read_excel('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_data_collection.xlsx', sheet_name='Sheet1')

# Keep all columns in df1 that start with "benefit_" and drop the rest of the columns
df1 = df1.filter(regex='^benefit_')

# Change column name "benefit_year" to "YEAR" to match other csv file
df1.rename(columns={'benefit_year': 'YEAR'}, inplace=True)

#print(df1.head)

#resassign cpi csv file to df2
df2 = df  #cpi
print(df2.head)

#convert year to int dt
df1['YEAR'] = pd.to_numeric(df1['YEAR'], errors='coerce', downcast='integer')
df2['YEAR'] = pd.to_numeric(df2['YEAR'], errors='coerce', downcast='integer')

#use year to merge dfs
merged_df = pd.merge(df1, df2[['YEAR', 'FACTOR']], on='YEAR', how='left')

df = merged_df

#use the merged output we just made
# Merge the two DataFrames on the 'country' and 'Country Name'
df3 = pd.read_csv('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_code/PPP.csv')
merged_df = pd.merge(df, df3, left_on='benefit_country', right_on='Country Name', how='left')

# Ensure that the year values in df are valid and aligned with the column names in df3
def get_ppp_value(row):
    # Try to access the column corresponding to the year
    year_column = str(int(row['YEAR']))  # Ensure the year is treated as a string (for column access)
    
    if year_column in row.index:  # Check if the column for the year exists
        return row[year_column]  # Return the value from the corresponding year column
    else:
        return np.nan  # If the column doesn't exist, return NaN

# Apply the function to get the 'ppp' values
merged_df['ppp'] = merged_df.apply(get_ppp_value, axis=1)
merged_df = merged_df.drop(columns=['Country Code',
       'Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963',
       '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
       '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981',
       '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990',
       '1991', '1992', '1993', '1994', '1995', '1996','1997', '1998', '1999', '2000','2001', '2002', '2003', '2004', '2005', '2006','2007', '2008', '2009', '2010', '2011','2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019','2020', '2021', '2022', '2023'])

# Ensure the columns being multiplied are of numeric type
merged_df['ppp'] = pd.to_numeric(merged_df['ppp'], errors='coerce')
merged_df['FACTOR'] = pd.to_numeric(merged_df['FACTOR'], errors='coerce')
merged_df['benefit_net'] = pd.to_numeric(merged_df['benefit_net'], errors='coerce')

merged_df['combinedfactor'] = merged_df['ppp'] * merged_df['FACTOR']
merged_df['netnew'] = merged_df['combinedfactor'] * merged_df['benefit_net']

# Print the result to check
merged_df.tail(100)

merged_df.to_csv('litreview_cleaneddata.csv')

#import main plot with everything


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('litreview_cleaneddata.csv')

# Define marker shapes for benefits
marker_map = {
    'health': 'o',      # Circle
    'productivity': 's', # Square
    'both': '^'          # Triangle
}

# Create a figure with a larger size
plt.figure(figsize=(16, 10))

# Subplots
# Final argument means we're working on subplot 1
plt.subplot(2, 2, 1)
plt.title('Net Economic Benefits of Ventilation')
filtration_mask = df['benefit_type'] == 'ventilation'
plt.scatter(df['benefit_citation'][filtration_mask], df['netnew'][filtration_mask], color='green', label='Filtration')
plt.ylim(-250, 6000)
plt.xticks(rotation=45, fontsize=8)
# Add a horizontal line at y=0
plt.axhline(0, color='grey', linestyle='--', linewidth=1, label='y=0')
plt.ylabel ('Net Benefit (USD per capita per year)')

# plt.plot()
# plt.legend(loc='upper right')

# Final argument means we're working on subplot 2
plt.subplot(2, 2, 2)
plt.title('Net Economic Benefits of Filtration')
filtration_mask = df['benefit_type'] == 'filtration'
plt.scatter(df['benefit_citation'][filtration_mask], df['netnew'][filtration_mask], color='green', label='Filtration')
plt.ylim(-250, 6000)
plt.xticks(rotation=45, fontsize=8)
# Add a horizontal line at y=0
plt.axhline(0, color='grey', linestyle='--', linewidth=1, label='y=0')
plt.ylabel ('Net Benefit (USD per capita per year)')

# plt.plot(time, amplitude_halved, label='sine2')
# plt.legend(loc='best')

# Final argument means we're working on subplot 3
plt.subplot(2, 2, 3)
#plt.legend()
plt.title('Net Economic Benefits of Source Control')
filtration_mask = df['benefit_type'] == 'source control'
plt.scatter(df['benefit_citation'][filtration_mask], df['netnew'][filtration_mask], color='green', label='Filtration')
plt.ylim(-250, 6000)
plt.xticks(rotation=45, fontsize=8)
# Add a horizontal line at y=0
plt.axhline(0, color='grey', linestyle='--', linewidth=1, label='y=0')
plt.ylabel ('Net Benefit (USD per capita per year)')
# plt.plot(time, amplitude_halved, label='sine2')
# plt.legend(loc='best')

# Final argument means we're working on subplot 4
plt.subplot(2, 2, 4)
plt.title('Net Economic Benefits of Combined-Type Interventions')
combination_mask = (df['benefit_type'] == 'combination') | (df['benefit_type'] == 'combined')
plt.scatter(df['benefit_citation'][filtration_mask], df['netnew'][filtration_mask], color='green', label='Filtration')
plt.ylim(-250, 6000)
plt.xticks(rotation=45, fontsize=8)
plt.ylabel ('Net Benefit (USD per capita per year)')
# Add a horizontal line at y=0
plt.axhline(0, color='grey', linestyle='--', linewidth=1, label='y=0')
# plt.plot(time, amplitude_halved, label='sine2')
# plt.legend(loc='best')

# Give some room around the figure by calling tight_layout() and passing a pad value
plt.tight_layout(pad=2)
plt.show()

#useful object-oriented approach methods:
#add_subplot() to add or retrieve an Axes



#keep all columns that start with the prefix "benefits_"
#drop "beneifts_" from all column names


#convert USA United States to _______



