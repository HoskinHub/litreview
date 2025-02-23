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
df1 = pd.read_csv('lit_data.csv', encoding='latin1')

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

# Import main plot with everything
df = pd.read_csv('litreview_cleaneddata.csv')

# Remove rows where 'benefit_citation' equals 'Zuraimi et al., 2007'
df = df[df['benefit_citation'] != 'Zuraimi, 2007']



# Define a mapping of pollutants to marker shapes
# Create a color map for pollutants
color_map = {'PM10': '#648FFF', 'NO2': '#785EF0', 'DEHP': '#DC267F', 'ozone': 'purple', 'PM2.5': '#FE6100', 'multiple': '#FFB000', 'radon': '#DC267F'}

# Define marker style based on the value in 'benefit_pollutant' and 'benefit_healthorprod'
def get_marker_style_and_fill(row):
    # Determine the base marker shape from 'benefit_pollutant'
    pollutant_marker_map = marker_map = {'PM10': 'o', 'NO2': 's', 'DEHP': '^', 'ozone': 'p', 'PM2.5': 'D', 'multiple': 'X', 'radon': 'P'}
    marker = pollutant_marker_map.get(row['benefit_pollutant'], 'o')  # Default to 'o' if no match

    # Adjust the fill style based on 'benefit_healthorprod'
    if row['benefit_healthorprod'] == 'health':
        # Filled marker
        return marker, True  # True means filled
    elif row['benefit_healthorprod'] == 'performance':
        # Hollow marker
        return marker, False  # False means hollow
    elif row['benefit_healthorprod'] == 'both':
        # Half-filled marker (use hatch pattern to simulate half-filled)
        return marker, 'half'  # 'half' represents a half-filled marker
    else:
        return marker, True  # Default to filled if no match

# Create a figure with a larger size
plt.figure(figsize=(18, 10))  # Adjusting the figure size to fit the tall subplots horizontally

# Sort the DataFrame by 'year' (benefit_year) in ascending order
df_sorted = df.sort_values(by='year', ascending=True)


# Subplot 1: Net Economic Benefits of Ventilation
plt.subplot(1, 4, 1)  # Adjusting to 1 row and 4 columns (first subplot)
plt.title('Ventilation')

# Apply the mask for 'ventilation' benefit type

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
    
    # Plot points for this pollutant using the corresponding marker
    sns.scatterplot(
        x=df_sorted['benefit_citation'][pollutant_mask], 
        y=df_sorted['netnew'][pollutant_mask], 
        marker=marker, 
        label=pollutant,
       #color=color_map[pollutant],  # Set the color of the marker
        #edgecolor=color_map[pollutant],  # Set the edge color to the same as the marker's color
        linewidth=1,  # Adjust the thickness of the outline if needed
        alpha=0.5  # Set transparency for the face of the marker
    )

# Formatting the plot
plt.ylim(-250, 2200)
plt.xticks(rotation=45, fontsize=8)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')
plt.xlabel(' ')

# Subplot 2: Net Economic Benefits of Filtration
plt.subplot(1, 4, 2)  # Adjusting to 1 row and 4 columns (second subplot)
plt.title('Filtration')

filtration_mask = df_sorted['benefit_type'] == 'filtration'

# Iterate through unique pollutants and plot with corresponding markers
for pollutant in df['benefit_pollutant'].unique():
    pollutant_mask = filtration_mask & (df['benefit_pollutant'] == pollutant)
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
    
    # Plot points for this pollutant using the corresponding marker
    sns.scatterplot(
        x=df_sorted['benefit_citation'][pollutant_mask], 
        y=df_sorted['netnew'][pollutant_mask], 
        marker=marker, 
        label=pollutant,
        #color=color_map[pollutant],  # Set the color of the marker
        #edgecolor=color_map[pollutant],  # Set the edge color to the same as the marker's color
        linewidth=1,  # Adjust the thickness of the outline if needed
        alpha=0.5  # Set transparency for the face of the marker
    )

# Formatting the plot
plt.ylim(-250, 2200)
plt.xticks(rotation=45, fontsize=8)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')
plt.xlabel(' ')

# Subplot 3: Net Economic Benefits of Source Control
plt.subplot(1, 4, 3)  # Adjusting to 1 row and 4 columns (third subplot)
plt.title('Source Control')

source_control_mask = df_sorted['benefit_type'] == 'source control'

# Iterate through unique pollutants and plot with corresponding markers
for pollutant in df['benefit_pollutant'].unique():
    source_control_mask = filtration_mask & (df['benefit_pollutant'] == pollutant)
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
    # Plot points for this pollutant using the corresponding marker
    sns.scatterplot(
        x=df_sorted['benefit_citation'][pollutant_mask], 
        y=df_sorted['netnew'][pollutant_mask], 
        marker=marker, 
        label=pollutant,
        #color=color_map[pollutant],  # Set the color of the marker
        #edgecolor=color_map[pollutant],  # Set the edge color to the same as the marker's color
        linewidth=1,  # Adjust the thickness of the outline if needed
        alpha=0.5  # Set transparency for the face of the marker
    )

# Formatting the plot
plt.ylim(-250, 2200)
plt.xticks(rotation=45, fontsize=8)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')
plt.xlabel(' ')

# Subplot 4: Net Economic Benefits of Combined-Type Interventions
plt.subplot(1, 4, 4)  # Adjusting to 1 row and 4 columns (fourth subplot)
plt.title('Combined Interventions')

combination_mask = (df_sorted['benefit_type'] == 'combination') | (df_sorted['benefit_type'] == 'combined')

# Iterate through unique pollutants and plot with corresponding markers
for pollutant in df['benefit_pollutant'].unique():
    pollutant_mask = combination_mask & (df['benefit_pollutant'] == pollutant)
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
    
    # Plot points for this pollutant using the corresponding marker
    sns.scatterplot(
        x=df_sorted['benefit_citation'][pollutant_mask], 
        y=df_sorted['netnew'][pollutant_mask], 
        marker=marker, 
        label=pollutant,
        #color=color_map[pollutant],  # Set the color of the marker
        #edgecolor=color_map[pollutant],  # Set the edge color to the same as the marker's color
        linewidth=1,  # Adjust the thickness of the outline if needed
        alpha=0.5  # Set transparency for the face of the marker
    )

# Formatting the plot
plt.ylim(-250, 2200)
plt.xticks(rotation=45, fontsize=8)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')
plt.xlabel(' ')

# Title and layout adjustments
plt.suptitle('Economic Net Benefits of IAQ Interventions of Different Types', fontsize=18, fontweight='bold', y=0.98)

# Give some room around the figure by calling tight_layout() and passing a pad value
plt.tight_layout(pad=2)
plt.show()
