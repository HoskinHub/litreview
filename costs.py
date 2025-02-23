#OneDrive - University of Toronto/zoes_project/lit_review_cba_iaq/lit_review_code/Costs.csv



import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#path to file in OneDrive
df = pd.read_csv('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_code/merged_data.csv')



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data

# Set Seaborn theme
sns.set_theme(style="ticks")

# Remove tall points
df = df[df['netnew'] <= 4000]
df.sort_values(by=['location', 'YEAR', 'citation'], inplace=True)  # Sort by location first

# Define color mapping for types
color_map = {
    'ventilation': 'blue',
    'filtration': 'green',
    'source control': 'orange',
    'combination': 'purple'
}

# Define marker shapes for benefits
marker_map = {
    'health': 'o',      # Circle
    'productivity': 's', # Square
    'both': '^'          # Triangle
}

# Create a figure
plt.figure(figsize=(12, 8))

# Unique locations for grouping
unique_locations = df['location'].unique()

# Scatter plot with colors based on type and shapes based on benefit
for location in unique_locations:
    loc_mask = df['location'] == location
    for type_, color in color_map.items():
        for benefit, marker in marker_map.items():
            mask = loc_mask & (df['type'] == type_) & (df['benefit'] == benefit)
            if mask.any():
                plt.scatter(
                    df['citation'][mask].repeat(df['n'][mask]).values,
                    df['netnew'][mask].repeat(df['n'][mask]).values,
                    color=color,
                    marker=marker,
                    zorder=1,
                    alpha=0.6,
                    s=60,
                    edgecolor=color,
                    linewidth=0.8,
                    label=type_ if benefit == 'health' else ""  # Only label the first occurrence of each type
                )

# Use this to avoid duplicate legend entries for color
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), title='Type', loc='upper right')

# Add labels and title
plt.xticks(rotation=90)
plt.ylabel('Net Benefit ($/person/year)', fontsize=14)
plt.title('Health and Productivity Benefits of Indoor Air Quality Interventions', fontsize=14)

# Add a horizontal line at y=0
plt.axhline(0, color='grey', linestyle='--', linewidth=1, label='y=0')

# Show plot
plt.tight_layout()
plt.show()



fig, ax = plt.subplots()
print(df.head(n=5))  #show the first few rows of data -- looks good

# Unique locations for grouping
unique_locations = df['location'].unique()

# Define color mapping for types
color_map = {
    'ventilation': 'blue',
    'filtration': 'green',
    'source control': 'orange',
    'combination': 'purple'
}

# Define marker shapes for benefits
marker_map = {
    'health': 'o',      # Circle
    'productivity': 's', # Square
    'both': '^'          # Triangle
}

# Scatter plot with colors based on type and shapes based on benefit
for location in unique_locations:
    loc_mask = df['location'] == location
    for type_, color in color_map.items():
        for benefit, marker in marker_map.items():
            mask = loc_mask & (df['type'] == type_) & (df['benefit'] == benefit)
            if mask.any():
                plt.scatter(
                    df['citation'][mask].repeat(df['n'][mask]).values,
                    df['netnew'][mask].repeat(df['n'][mask]).values,
                    color=color,
                    marker=marker,
                    zorder=1,
                    alpha=0.6,
                    s=60,
                    edgecolor=color,
                    linewidth=0.8,
                    label=type_ if benefit == 'health' else ""  # Only label the first occurrence of each type
                )

# Use this to avoid duplicate legend entries for color
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), title='Type', loc='upper left')

plt.show()  # Ensure the figure is displayed correctly