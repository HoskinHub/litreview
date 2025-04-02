import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Import CPI CSV file from OneDrive
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

# Remove unnecessary columns
merged_df = merged_df.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'])

# Ensure the columns being multiplied are of numeric type
merged_df['ppp'] = pd.to_numeric(merged_df['ppp'], errors='coerce')
merged_df['FACTOR'] = pd.to_numeric(merged_df['FACTOR'], errors='coerce')
merged_df['benefit_net'] = pd.to_numeric(merged_df['benefit_net'], errors='coerce')

# Create combined factor and net new value
merged_df['combinedfactor'] = merged_df['ppp'] * merged_df['FACTOR']
merged_df['netnew'] = merged_df['combinedfactor'] * merged_df['benefit_net']

# Import main plot with everything
df = pd.read_csv('litreview_cleaneddata.csv')

# Remove rows where 'benefit_citation' equals 'Zuraimi et al., 2007'
df = df[df['benefit_citation'] != 'Zuraimi, 2007']

# Define a mapping of pollutants to marker shapes
marker_map = {'PM10': 'D', 'NO2': 'X', 'DEHP': '^', 'ozone': 'p', 'PM2.5': 'o', 'multiple': 's', 'radon': 'P'}
color_map = {'PM10': '#648FFF', 'NO2': '#785EF0', 'DEHP': '#DC267F', 'ozone': 'purple', 'PM2.5': '#FE6100', 'multiple': '#FFB000', 'radon': '#DC267F'}

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

# Apply the mask for 'ventilation' benefit type
ventilation_mask = df['benefit_type'] == 'ventilation'
filtration_mask = df['benefit_type'] == 'filtration '
sourcecontrol_mask = df['benefit_type'] == 'source control'
combination_mask = df['benefit_type'] == 'combination'

# Create a figure with subplots
fig, axes = plt.subplots(1, 4, figsize=(18, 10))  # Create 1 row and 4 columns

# List of subplot titles and respective masks (Adjust as per your data structure)
subplots_info = [
    ('Filtration', filtration_mask),
    ('Ventilation', ventilation_mask),
    ('Source Control', sourcecontrol_mask),
    ('Combination of Interventions', combination_mask)
]

# Loop through each subplot for i, (title, mask) in enumerate(subplots_info):
for i, (title, mask) in enumerate(subplots_info):
    ax = axes[i]  # Get the current axis
    ax.set_title(title)  # Set title for the subplot
    
    # Iterate through each row in the filtered dataframe for the current mask
    for index, row in df[mask].iterrows():
        pollutant = row['benefit_pollutant']
        benefit_healthorprod = row['benefit_healthorprod']

        # Get the marker for the pollutant
        marker = marker_map.get(pollutant, 'o')  # Default to 'o' if pollutant is not in map
        color = color_map.get(pollutant, '#000000')  # Default to black if pollutant is not in map

        # Determine if the marker should be filled, hollow, or half-filled
        fill_type = get_marker_style_and_fill(row)[1]  # 'True' for filled, 'False' for hollow, 'half' for hatch

        if fill_type == True:  # Filled marker
            ax.scatter(row['benefit_citation'], row['benefit_net'], s=50, marker=marker, alpha=0.7,
                       edgecolors=color, facecolors=color)  # Facecolor filled
        elif fill_type == False:  # Hollow marker
            ax.scatter(row['benefit_citation'], row['benefit_net'], s=50, marker=marker, alpha=0.7,
                       edgecolors=color, facecolors='none')  # Hollow (no fill)
        elif fill_type == 'half':  # Half-filled marker (simulating with hatch)
            ax.scatter(row['benefit_citation'], row['benefit_net'], s=50, marker=marker, alpha=0.7,
                       edgecolors=color, facecolors=color, hatch='//')  # Hatch to simulate half-fill
    
    # Formatting the plot
    ax.set_ylim(-250, 2200)
    ax.axhline(0, color='grey', linestyle='--', linewidth=1)
    ax.set_ylabel('Net Benefit (USD per capita per year)', fontsize=16)
    ax.set_xlabel(' ')

# Adjust layout to prevent overlap
plt.tight_layout()

# Display the final plot
plt.show()
