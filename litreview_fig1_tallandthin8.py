import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load and process data
df = pd.read_csv('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_code/CPI USA PPP.csv', encoding='latin1')
df['year'] = df['DATE'].str[:4]
yearly_median = df.groupby('year')['CPIAUCSL'].median()
df['MEDFORYEAR'] = df['year'].map(yearly_median)
med_for_2024 = df[df['year'] == '2024']['MEDFORYEAR'].iloc[0]
df['FACTOR'] = (med_for_2024 / df['MEDFORYEAR'])

df1 = pd.read_csv('lit_data.csv', encoding='latin1')
df1 = df1.filter(regex='^benefit_')
df1.rename(columns={'benefit_year': 'year'}, inplace=True)
df1['year'] = pd.to_numeric(df1['year'], errors='coerce', downcast='integer')
df['year'] = pd.to_numeric(df['year'], errors='coerce', downcast='integer')

merged_df = pd.merge(df1, df[['year', 'FACTOR']], on='year', how='left')
df2 = pd.read_csv('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_code/PPP.csv')
merged_df = pd.merge(merged_df, df2, left_on='benefit_country', right_on='Country Name', how='left')

def get_ppp_value(row):
    year_column = str(int(row['year']))
    return row[year_column] if year_column in row.index else np.nan

merged_df['ppp'] = merged_df.apply(get_ppp_value, axis=1)
merged_df = merged_df.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'])
merged_df['ppp'] = pd.to_numeric(merged_df['ppp'], errors='coerce')
merged_df['FACTOR'] = pd.to_numeric(merged_df['FACTOR'], errors='coerce')
merged_df['benefit_net'] = pd.to_numeric(merged_df['benefit_net'], errors='coerce')
merged_df['combinedfactor'] = merged_df['ppp'] * merged_df['FACTOR']
merged_df['netnew'] = merged_df['combinedfactor'] * merged_df['benefit_net']

# Create a combined map for pollutants
combined_map = {
    'PM10': {'marker': 'D', 'color': '#648FFF'},
    'NO2': {'marker': 'X', 'color': '#785EF0'},
    'DEHP': {'marker': '^', 'color': '#DC267F'},
    'ozone': {'marker': 'p', 'color': 'purple'},
    'PM2.5': {'marker': 'o', 'color': '#FE6100'},
    'multiple': {'marker': 's', 'color': '#FFB000'},
    'radon': {'marker': 'P', 'color': '#DC267F'}
}

# Function to create subplots
def create_subplot(ax, mask, title):
    ax.set_title(title)
    
    for pollutant, properties in combined_map.items():
        pollutant_mask = mask & (df_sorted['benefit_pollutant'] == pollutant)
        
        for index, row in df_sorted[pollutant_mask].iterrows():
            benefit_type = row['benefit_type']
            
            # Adjust marker style based on benefit type
            if benefit_type == 'health':
                facecolors = properties['color']
                edgecolors = properties['color']
            elif benefit_type == 'performance':
                facecolors = 'none'
                edgecolors = properties['color']
            elif benefit_type == 'both':
                facecolors = 'none'
                edgecolors = properties['color']
                ax.scatter(row['benefit_citation'], row['benefit_net'], s=50, marker=properties['marker'], alpha=0.5, hatch='x')
                continue  # Skip to avoid double plotting
            ax.scatter(row['benefit_citation'], row['benefit_net'], s=50, marker=properties['marker'], alpha=0.5)

    ax.set_ylim(-250, 2200)
    ax.axhline(0, color='grey', linestyle='--', linewidth=1)
    #ax.set_xticks(range(len(df)))  # Set the tick positions
    #ax.set_xticklabels(labels=['benefit_citation'], rotation=45, ha='right', fontsize=8) 
    ax.set_ylabel('Net Benefit (USD per capita per year)', fontsize=16)
    ax.set_xlabel(' ')

# Create figure and subplots
plt.figure(figsize=(18, 10))
df_sorted = merged_df.sort_values(by='year', ascending=True)

# Ventilation subplot
ax1 = plt.subplot(1, 4, 1)
ventilation_mask = df_sorted['benefit_type'] == 'ventilation'
create_subplot(ax1, ventilation_mask, 'Ventilation')

# Filtration subplot
ax2 = plt.subplot(1, 4, 2)
filtration_mask = df_sorted['benefit_type'] == 'filtration'
create_subplot(ax2, filtration_mask, 'Filtration')

# Source Control subplot
ax3 = plt.subplot(1, 4, 3)
source_control_mask = df_sorted['benefit_type'] == 'source control'
create_subplot(ax3, source_control_mask, 'Source Control')

# Combined Interventions subplot
ax4 = plt.subplot(1, 4, 4)
combination_mask = (df_sorted['benefit_type'] == 'combination') | (df_sorted['benefit_type'] == 'combined')
create_subplot(ax4, combination_mask, 'Combined Interventions')

# Adjust layout and spacing
plt.tight_layout(pad=2)
plt.subplots_adjust(hspace=0.3, wspace=0.2)
plt.suptitle('Economic Net Benefits of IAQ Interventions of Different Types', fontsize=18, fontweight='bold', y=0.98)

# Show plot
plt.show()
