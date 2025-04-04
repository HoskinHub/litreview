import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Pollutant marker and color maps
marker_map = {'PM10': 'D', 'PM2.5': 'o', 'multiple': 's'}
color_map = {'PM10': '#648FFF', 'PM2.5': '#882255', 'multiple': '#FFB000'}

# Create custom legend handles
legend_handles = []
for pollutant in marker_map:
    marker = marker_map[pollutant]
    color = color_map[pollutant]
    
    # Use LaTeX for subscripts in the pollutant labels
    if 'PM' in pollutant:
        pollutant_label = r'$\text{PM}_{' + pollutant[2:] + '}$'  # For PM10 and PM2.5
    else:
        pollutant_label = pollutant  # Other pollutants

    # Create a custom Line2D legend entry for each pollutant
    legend_handles.append(Line2D([0], [0], marker=marker, color='w', markerfacecolor=color, markersize=10, label=pollutant_label))

# Create a plot for demonstration
plt.figure(figsize=(8, 6))
plt.scatter(range(10), range(10), color='r')  # Dummy scatter to create a plot

# Add the legend using the custom handles
plt.legend(handles=legend_handles, title='Pollutants', loc='upper left', fontsize=10)

# Show the plot
plt.show()
