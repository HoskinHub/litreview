import matplotlib.pyplot as plt
import pandas as pd

df_sorted = pd.read_csv('litreview/litreview_cleaneddata_ASHRAE.csv')

# Define a mapping of pollutants to marker shapes
marker_map = {'PM10': 'D', 'NO2': 'X', 'DEHP': '^', 'ozone': 'p', 'PM2.5': 'o', 'multiple': 's', 'radon': 'P'}
color_map = {'PM10': '#648FFF', 'NO2': '#FD774B', 'DEHP': '#117733', 'ozone': '#88CCEE', 'PM2.5': '#882255', 'multiple': '#FFB000', 'radon': '#88CCEE'}

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
ventilation_mask = df_sorted['benefit_type'] == 'ventilation'
filtration_mask = df_sorted['benefit_type'] == 'filtration '
sourcecontrol_mask = df_sorted['benefit_type'] == 'source control'
combination_mask = df_sorted['benefit_type'] == 'combination'


# Create a figure with a larger size
plt.figure(figsize=(18, 10))  # Adjusting the figure size to fit the tall subplots horizontally

# Subplot 1: Net Economic Benefits of Ventilation
plt.subplot(1, 3, 1)  # Adjusting to 1 row and 4 columns (first subplot)
plt.title('Ventilation', fontsize=14)
# Iterate through each row in the filtered dataframe
for index, row in df_sorted[ventilation_mask].iterrows():
    pollutant = row['benefit_pollutant']
    benefit_healthorprod = row['benefit_healthorprod']
    
    # Get the marker for the pollutant
    marker = marker_map.get(pollutant, 'o')  # Default to 'o' if pollutant is not in map
    color = color_map.get(pollutant, '#000000')  # Default to black if pollutant is not in map
    
    # Determine if the marker should be filled, hollow, or half-filled
    fill_type = get_marker_style_and_fill(row)[1]  # 'True' for filled, 'False' for hollow, 'half' for hatch
    
    if fill_type == True:  # Filled marker
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=60, marker=marker, alpha=0.7, linewidths=0.8,
                    edgecolors=color, facecolors=color)  # Facecolor filled
    elif fill_type == False:  # Hollow marker
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=60, marker=marker, alpha=0.7, linewidths=0.8,
                    edgecolors=color, facecolors='none')  # Hollow (no fill)
    elif fill_type == 'half':  # Half-filled marker (simulating with hatch)
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=60, marker=marker, alpha=0.7, linewidths=0.8,
                    edgecolors=color, facecolors='none', hatch='///////')
        # Simulate half-fill with a hatch pattern
        circle = plt.Circle((row['benefit_citation'], row['benefit_net']), 0.3, color=color, alpha=0.0, hatch='//')
        plt.gca().add_artist(circle)
    
# Formatting the plot
plt.ylim(-150, 1700)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.ylabel('Net Benefit (USD per capita per year)', fontsize=16)
plt.xlabel(' ')

# Subplot 1: Net Economic Benefits of Ventilation
plt.subplot(1, 3, 3)  # Adjusting to 1 row and 4 columns (first subplot)
plt.title('Filtration', fontsize=14)

# Iterate through each row in the filtered dataframe
for index, row in df_sorted[filtration_mask].iterrows():
    pollutant = row['benefit_pollutant']
    benefit_healthorprod = row['benefit_healthorprod']
    
    # Get the marker for the pollutant
    marker = marker_map.get(pollutant, 'o')  # Default to 'o' if pollutant is not in map
    color = color_map.get(pollutant, '#000000')  # Default to black if pollutant is not in map
    
    # Determine if the marker should be filled, hollow, or half-filled
    fill_type = get_marker_style_and_fill(row)[1]  # 'True' for filled, 'False' for hollow, 'half' for hatch
    
    if fill_type == True:  # Filled marker
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=60, marker=marker, alpha=0.7, linewidths=0.8,
                    edgecolors=color, facecolors=color)  # Facecolor filled
    elif fill_type == False:  # Hollow marker
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=60, marker=marker, alpha=0.7, linewidths=0.8,
                    edgecolors=color, facecolors='none')  # Hollow (no fill)
    elif fill_type == 'half':  # Half-filled marker (simulating with hatch)
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=60, marker=marker, alpha=0.7, linewidths=0.8,
                    edgecolors=color, facecolors='none', hatch='///////')  # Hatch to simulate half-fill

# Formatting the plot
plt.ylim(-150, 1700)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.xlabel(' ')


# Subplot 1: Net Economic Benefits of Ventilation
plt.subplot(1, 3, 2)  # Adjusting to 1 row and 4 columns (first subplot)
plt.title('Combination of Interventions', fontsize=14)
# Iterate through each row in the filtered dataframe
for index, row in df_sorted[combination_mask].iterrows():
    pollutant = row['benefit_pollutant']
    benefit_healthorprod = row['benefit_healthorprod']
    
    # Get the marker for the pollutant
    marker = marker_map.get(pollutant, 'o')  # Default to 'o' if pollutant is not in map
    color = color_map.get(pollutant, '#000000')  # Default to black if pollutant is not in map
    
    # Determine if the marker should be filled, hollow, or half-filled
    fill_type = get_marker_style_and_fill(row)[1]  # 'True' for filled, 'False' for hollow, 'half' for hatch
    
    if fill_type == True:  # Filled marker
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=50, marker=marker, alpha=0.8, linewidths=1,
                    edgecolors=color, facecolors=color)  # Facecolor filled
    elif fill_type == False:  # Hollow marker
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=50, marker=marker, alpha=0.8, linewidths=1,
                    edgecolors=color, facecolors='none')  # Hollow (no fill)
    elif fill_type == 'half':  # Half-filled marker (simulating with hatch)
        plt.scatter(row['benefit_citation'], row['benefit_net'], s=50, marker=marker, alpha=0.8, linewidths=1,
                    edgecolors=color, facecolors='none', hatch='///////')  # Hatch to simulate half-fill


# Formatting the plot
plt.ylim(-150, 1700)
plt.xticks(rotation=45, ha='right', fontsize=12)  # Adjust the x-position slightly
plt.axhline(0, color='grey', linestyle='--', linewidth=1)
plt.xlabel(' ')

# Subplot 1: Net Economic Benefits of Ventilation
ax1 = plt.subplot(1, 3, 1)
# Set the vertical spines (left and right) to grey for this subplot
ax1.spines['left'].set_edgecolor('black')
ax1.spines['right'].set_edgecolor('#D3D3D3')
ax1.spines['left'].set_linewidth(1)
ax1.spines['right'].set_linewidth(0.5)

# Subplot 2: Net Economic Benefits of Filtration
ax2 = plt.subplot(1, 3, 2)
ax2.set_yticklabels([])
# Set the vertical spines (left and right) to grey for this subplot
ax2.spines['left'].set_edgecolor('#D3D3D3')
ax2.spines['right'].set_edgecolor('#D3D3D3')
ax2.spines['left'].set_linewidth(1)
ax2.spines['right'].set_linewidth(1)

# Subplot 4: Net Economic Benefits of Combined-Type Interventions
ax3 = plt.subplot(1, 3, 3)
ax3.set_yticklabels([])
# Set the vertical spines (left and right) to grey for this subplot
ax3.spines['left'].set_edgecolor('#D3D3D3')
ax3.spines['right'].set_edgecolor('black')
ax3.spines['left'].set_linewidth(0.5)
ax3.spines['right'].set_linewidth(1)

# Give some room around the figure by calling tight_layout() and passing a pad value
plt.tight_layout(pad=2)
plt.subplots_adjust(hspace=0.3, wspace=0.1)  # Adjust spacing between subplots
plt.show()



