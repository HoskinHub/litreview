#marker and fill

#litreview_fig1_tallandthin2.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Import CPI CSV file
df = pd.read_csv('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_code/CPI USA PPP.csv', encoding='latin1')

# Get median CPI per year
df['year'] = df['DATE'].str[:4]
yearly_median = df.groupby('year')['CPIAUCSL'].median()
df['MEDFORYEAR'] = df['year'].map(yearly_median)

# Calculate percent differences between CPIs
med_for_2024 = df[df['year'] == '2024']['MEDFORYEAR'].iloc[0]

# Transform the 'CPIAUCSL' values for each year relative to the 2024 CPI
df['FACTOR'] = (med_for_2024 / df['MEDFORYEAR'])

# Import data collection Excel file
df1 = pd.read_csv('litreview/lit_data.csv', encoding='latin1')

# Keep all columns in df1 that start with "benefit_" and drop the rest of the columns
df1 = df1.filter(regex='^benefit_')

# Change column name "benefit_year" to "year" to match other CSV file
df1.rename(columns={'benefit_year': 'year'}, inplace=True)

# Convert year to int dtype
df1['year'] = pd.to_numeric(df1['year'], errors='coerce', downcast='integer')
df['year'] = pd.to_numeric(df['year'], errors='coerce', downcast='integer')

# Merge the two DataFrames on the 'year' column
merged_df = pd.merge(df1, df[['year', 'FACTOR']], on='year', how='left')

# Merge with PPP data
df2 = pd.read_csv('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_code/PPP.csv')
merged_df = pd.merge(merged_df, df2, left_on='benefit_country', right_on='Country Name', how='left')

# Ensure that the year values in df are valid and aligned with the column names in df2
def get_ppp_value(row):
    year_column = str(int(row['year']))  # Ensure the year is treated as a string (for column access)
    if year_column in row.index:  # Check if the column for the year exists
        return row[year_column]  # Return the value from the corresponding year column
    else:
        return np.nan  # If the column doesn't exist, return NaN

# Apply the function to get the 'ppp' values
merged_df['ppp'] = merged_df.apply(get_ppp_value, axis=1)
merged_df = merged_df.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'])

# Ensure the columns being multiplied are of numeric type
merged_df['ppp'] = pd.to_numeric(merged_df['ppp'], errors='coerce')
merged_df['FACTOR'] = pd.to_numeric(merged_df['FACTOR'], errors='coerce')
merged_df['benefit_net'] = pd.to_numeric(merged_df['benefit_net'], errors='coerce')

merged_df['combinedfactor'] = merged_df['ppp'] * merged_df['FACTOR']
merged_df['netnew'] = merged_df['combinedfactor'] * merged_df['benefit_net']

# Print the result to check
print(merged_df.tail(100))

merged_df.to_csv('litreview_cleaneddata.csv')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Import data (same CSV files as in your code)
df = pd.read_csv('litreview_cleaneddata.csv')

# Remove specific unwanted rows
df = df[df['benefit_citation'] != 'Zuraimi, 2007']

# Define a mapping of pollutants to marker shapes and their respective colors
color_map = {'PM10': '#648FFF', 'NO2': '#785EF0', 'DEHP': '#DC267F', 'ozone': 'purple', 'PM2.5': '#FE6100', 'multiple': '#FFB000', 'radon': '#DC267F'}
marker_map = {'PM10': 'o', 'NO2': 's', 'DEHP': '^', 'ozone': 'p', 'PM2.5': 'D', 'multiple': 'X', 'radon': 'P'}

# Define marker style based on 'benefit_healthorprod'
def get_marker_style_and_fill(row):
    # Determine marker shape from 'benefit_pollutant'
    marker = marker_map.get(row['benefit_pollutant'], 'o')  # Default to 'o' if no match

    # Determine fill style based on 'benefit_healthorprod'
    if row['benefit_healthorprod'] == 'health':
        return marker, True  # Filled marker
    elif row['benefit_healthorprod'] == 'performance':
        return marker, False  # Hollow marker
    elif row['benefit_healthorprod'] == 'both':
        return marker, 'half'  # Half-filled marker (using hatch)
    else:
        return marker, True  # Default to filled if no match

# Create a figure with a larger size (to fit all subplots)
plt.figure(figsize=(18, 10))  # Adjusting the figure size to fit the plots

# Subplot 1: Ventilation
plt.subplot(2, 2, 1)
plt.title('Ventilation')
ventilation_mask = df['benefit_type'] == 'ventilation'

# Iterate through unique pollutants and plot with corresponding markers
for pollutant in df['benefit_pollutant'].unique():
    pollutant_mask = ventilation_mask & (df['benefit_pollutant'] == pollutant)
    for index, row in df[pollutant_mask].iterrows():
        marker, is_filled = get_marker_style_and_fill(row)
        # Plot with appropriate marker style
        if is_filled == True:
            sns.scatterplot(x=[row['benefit_citation']], y=[row['netnew']], marker=marker, label=pollutant if index == df[pollutant_mask].index[0] else "", 
                             edgecolor='black', facecolor=color_map.get(pollutant, 'black'), legend=False)
        elif is_filled == False:
            sns.scatterplot(x=[row['benefit_citation']], y=[row['netnew']], marker=marker, label=pollutant if index == df[pollutant_mask].index[0] else "", 
                             edgecolor='black', facecolor='none', legend=False)
        elif is_filled == 'half':
            plt.scatter([row['benefit_citation']], [row['netnew']], marker=marker, edgecolor='black', facecolor='white', hatch='/', 
                        label=pollutant if index == df[pollutant_mask].index[0] else "")

plt.ylim(-250, 6000)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.xticks(rotation=45, fontsize=8)
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')

# Subplot 2: Filtration
plt.subplot(2, 2, 2)
plt.title('Filtration')
filtration_mask = df['benefit_type'] == 'filtration'

for pollutant in df['benefit_pollutant'].unique():
    pollutant_mask = filtration_mask & (df['benefit_pollutant'] == pollutant)
    for index, row in df[pollutant_mask].iterrows():
        marker, is_filled = get_marker_style_and_fill(row)
        if is_filled == True:
            sns.scatterplot(x=[row['benefit_citation']], y=[row['netnew']], marker=marker, label=pollutant if index == df[pollutant_mask].index[0] else "", 
                             edgecolor='black', facecolor=color_map.get(pollutant, 'black'), legend=False)
        elif is_filled == False:
            sns.scatterplot(x=[row['benefit_citation']], y=[row['netnew']], marker=marker, label=pollutant if index == df[pollutant_mask].index[0] else "", 
                             edgecolor='black', facecolor='none', legend=False)
        elif is_filled == 'half':
            plt.scatter([row['benefit_citation']], [row['netnew']], marker=marker, edgecolor='black', facecolor='white', hatch='/', 
                        label=pollutant if index == df[pollutant_mask].index[0] else "")

plt.ylim(-250, 6000)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.xticks(rotation=45, fontsize=8)
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')

# Subplot 3: Source Control
plt.subplot(2, 2, 3)
plt.title('Source Control')
source_control_mask = df['benefit_type'] == 'source control'

for pollutant in df['benefit_pollutant'].unique():
    pollutant_mask = source_control_mask & (df['benefit_pollutant'] == pollutant)
    for index, row in df[pollutant_mask].iterrows():
        marker, is_filled = get_marker_style_and_fill(row)
        if is_filled == True:
            sns.scatterplot(x=[row['benefit_citation']], y=[row['netnew']], marker=marker, label=pollutant if index == df[pollutant_mask].index[0] else "", 
                             edgecolor='black', facecolor=color_map.get(pollutant, 'black'), legend=False)
        elif is_filled == False:
            sns.scatterplot(x=[row['benefit_citation']], y=[row['netnew']], marker=marker, label=pollutant if index == df[pollutant_mask].index[0] else "", 
                             edgecolor='black', facecolor='none', legend=False)
        elif is_filled == 'half':
            plt.scatter([row['benefit_citation']], [row['netnew']], marker=marker, edgecolor='black', facecolor='white', hatch='/', 
                        label=pollutant if index == df[pollutant_mask].index[0] else "")

plt.ylim(-250, 6000)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.xticks(rotation=45, fontsize=8)
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')

# Subplot 4: Combined Interventions
plt.subplot(2, 2, 4)
plt.title('Combined Interventions')
combination_mask = (df['benefit_type'] == 'combination') | (df['benefit_type'] == 'combined')

for pollutant in df['benefit_pollutant'].unique():
    pollutant_mask = combination_mask & (df['benefit_pollutant'] == pollutant)
    for index, row in df[pollutant_mask].iterrows():
        marker, is_filled = get_marker_style_and_fill(row)
        if is_filled == True:
            sns.scatterplot(x=[row['benefit_citation']], y=[row['netnew']], marker=marker, label=pollutant if index == df[pollutant_mask].index[0] else "", 
                             edgecolor='black', facecolor=color_map.get(pollutant, 'black'), legend=False)
        elif is_filled == False:
            sns.scatterplot(x=[row['benefit_citation']], y=[row['netnew']], marker=marker, label=pollutant if index == df[pollutant_mask].index[0] else "", 
                             edgecolor='black', facecolor='none', legend=False)
        elif is_filled == 'half':
            plt.scatter([row['benefit_citation']], [row['netnew']], marker=marker, edgecolor='black', facecolor='white', hatch='/', 
                        label=pollutant if index == df[pollutant_mask].index[0] else "")

plt.ylim(-250, 6000)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.xticks(rotation=45, fontsize=8)
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')

# Title and layout adjustments
plt.suptitle('Net Economic Benefits of IAQ Interventions by Type', fontsize=18, fontweight='bold', y=0.98)
# Give some room around the figure by calling tight_layout() and passing a pad value
plt.tight_layout(pad=2)
plt.show()

