import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Assuming merged_df has the necessary columns ('benefit_healthorprod', 'benefit_type', etc.)

# Define marker styles based on the 'benefit_healthorprod' column
def get_marker_style(row):
    """Returns the marker style based on the 'benefit_healthorprod' column."""
    if row['benefit_healthorprod'] == 'health':
        return 'o', 'full'  # Filled circle
    elif row['benefit_healthorprod'] == 'productivity':
        return 'o', 'none'  # Empty circle
    elif row['benefit_healthorprod'] == 'combination':
        return 'o', 'half'  # Half-filled circle (we can use a custom style here)
    else:
        return 'o', 'full'  # Default to filled if not specified

# Apply the function to create a new column for marker styles
merged_df[['marker', 'fill_style']] = merged_df.apply(get_marker_style, axis=1, result_type="expand")

# Now let's plot with these markers
plt.figure(figsize=(16, 10))

# Define a mapping of pollutants to marker shapes (can be expanded as needed)
marker_map = {'pm': 'o', 'nox': 's', 'dehp': '^'}

# Subplot 1: Net Economic Benefits of Ventilation
plt.subplot(2, 2, 1)
plt.title('Net Economic Benefits of Ventilation')

# Apply the mask for 'ventilation' benefit type
ventilation_mask = merged_df['benefit_type'] == 'ventilation'

# Iterate through unique pollutants and plot with corresponding markers
for pollutant, marker in marker_map.items():
    # Filter the data for each pollutant
    pollutant_mask = ventilation_mask & (merged_df['benefit_pollutant'] == pollutant)
    
    # Iterate through the rows and plot each point with the correct marker style
    for _, row in merged_df[pollutant_mask].iterrows():
        marker_style = row['marker']
        fill_style = row['fill_style']
        
        # Determine the 'fill' or 'empty' based on 'fill_style' (customizing as needed)
        if fill_style == 'full':
            plt.scatter(
                row['benefit_citation'], 
                row['netnew'], 
                marker=marker_style, 
                facecolors='blue',  # Filled color
                edgecolors='black', 
                label=pollutant if 'pm' not in plt.gca().get_legend_handles_labels()[1] else ""
            )
        elif fill_style == 'none':
            plt.scatter(
                row['benefit_citation'], 
                row['netnew'], 
                marker=marker_style, 
                facecolors='none',  # Empty circle
                edgecolors='blue', 
                label=pollutant if 'pm' not in plt.gca().get_legend_handles_labels()[1] else ""
            )
        # For half-filled marker (combination type)
        elif fill_style == 'half':
            # We will use a custom approach for half-filled circles
            # For simplicity, let's use a different color or style (e.g., red)
            plt.scatter(
                row['benefit_citation'], 
                row['netnew'], 
                marker=marker_style, 
                facecolors='orange',  # Half-filled style (orange for this example)
                edgecolors='black', 
                label=pollutant if 'pm' not in plt.gca().get_legend_handles_labels()[1] else ""
            )

# Formatting the plot
plt.ylim(-250, 6000)
plt.xticks(rotation=45, fontsize=8)
plt.axhline(0, color='grey', linestyle='--', linewidth=1, label='y=0')
plt.ylabel('Net Benefit (USD per capita per year)')
plt.legend(title='Pollutants')

# You can repeat this same approach for your other subplots
# Repeat the same process for other benefit types like 'filtration', 'source control', etc.

plt.tight_layout(pad=2)
plt.show()
