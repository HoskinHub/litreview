import matplotlib.pyplot as plt
import pandas as pd

df_sorted = pd.read_csv('litreview/litreview_cleaneddata_ASHRAE.csv')

# List of benefit types to loop through
benefit_types = ['ventilation', 'filtration', 'combination']

# Loop through each benefit type and calculate the median of 'benefit_netnew'
for benefit_type in benefit_types:
    benefit_data = df_sorted[df_sorted['benefit_type'] == benefit_type]
    median_benefit_netnew = benefit_data['benefit_netnew'].median()
    print(f"Median benefit of {benefit_type}: {median_benefit_netnew}")

# List of benefit types to loop through
benefit_types = ['ventilation', 'filtration', 'combination']

# Loop through each benefit type and calculate the percentage of rows where 'benefit_netnew' > 0
for benefit_type in benefit_types:
    benefit_data = df_sorted[df_sorted['benefit_type'] == benefit_type]
    
    # Count the number of rows where 'benefit_netnew' > 0
    count_greater_than_zero = (benefit_data['benefit_netnew'] > 0).sum()
    
    # Calculate the total number of rows for this benefit type
    total_rows = len(benefit_data)
    
    # Calculate the percentage
    percentage = (count_greater_than_zero / total_rows) * 100
    
    # Print the result
    print(f"Percentage of rows with benefit_netnew > 0 for {benefit_type}: {percentage:.2f}%")

import pandas as pd

# Data for median benefit and percentage of rows
data = {
    "Benefit Type": ["Ventilation", "Filtration", "Combination"],
    "Median Benefit": [130.0, 46.8121021, 9.4359529255],
    "Percentage of Rows > 0 (%)": [95.24, 91.67, 78.57]
}

# Create a DataFrame
df_summary = pd.DataFrame(data)

# Display the table
print(df_summary)
# Save the summary DataFrame to a CSV file
df_summary.to_csv('litreview/benefit_summary.csv', index=False)
# Print the summary DataFrame to check
