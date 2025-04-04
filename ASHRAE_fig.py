import matplotlib.pyplot as plt
import pandas as pd

merged_df = pd.read_csv('litreview/litreview_cleaneddata_ASHRAE.csv')


import matplotlib.pyplot as plt
import pandas as pd

# Placeholder function for marker style and fill type (adjust this as necessary)
def get_marker_style_and_fill(row):
    # Example logic (replace with your actual logic for marker shape and fill type)
    marker = 'o'  # Default to circle
    fill_type = row['benefit_healthorprod']  # This can be True, False, or 'half'
    return marker, fill_type

# Set up the figure and axis
plt.figure(figsize=(10, 6))

# Loop through each row in the DataFrame and plot based on the conditions
for _, row in merged_df.iterrows():
    # Ensure data is valid for plotting (check if 'benefit_citation' and 'benefit_net' are not NaN)
    if pd.notna(row['benefit_citation']) and pd.notna(row['benefit_netnew']):
        
        # Determine marker style and fill type
        marker, fill_type = get_marker_style_and_fill(row)
        
        # Set color based on the 'benefit_pollutant' column (default to blue for simplicity)
        color = 'blue'  # This should be dynamically assigned based on 'benefit_pollutant'
        
        # Plot based on fill type
        if fill_type == True:  # Filled marker
            plt.scatter(row['benefit_citation'], row['benefit_netnew'], s=30, marker=marker, alpha=0.7, linewidths=0.8,
                        edgecolors=color, facecolors=color)
        elif fill_type == False:  # Hollow marker
            plt.scatter(row['benefit_citation'], row['benefit_netnew'], s=30, marker=marker, alpha=0.7, linewidths=0.8,
                        edgecolors=color, facecolors='none')
        elif fill_type == 'half':  # Half-filled marker (simulating with hatch)
            plt.scatter(row['benefit_citation'], row['benefit_netnew'], s=30, marker=marker, alpha=0.7, linewidths=0.8,
                        edgecolors=color, facecolors='none', hatch='///////')
            # Simulate half-fill with a hatch pattern
            circle = plt.Circle((row['benefit_citation'], row['benefit_netnew']), 0.3, color=color, alpha=0.0, hatch='//')
            plt.gca().add_artist(circle)

# Customize plot for the three sections
plt.axvline(x=0, color='gray', linestyle='--', label='Filtration')  # Left section divider
plt.axvline(x=5, color='gray', linestyle='--', label='Combination')  # Middle section divider

# Add labels and title
plt.xlabel('Benefit Citation')
plt.ylabel('Benefit Net')
plt.title('Scatterplot: Benefit Citation vs. Benefit Net')

# Show the plot
plt.legend()
plt.show()
