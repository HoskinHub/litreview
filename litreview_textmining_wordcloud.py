

import glob
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Path to the directory containing the .txt files
txt_dir = "/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_papers/lit_review_papers_for_data_collection/lit_review_papers_data_extracted"

# Get a list of all .txt files in the directory
txt_files = glob.glob(txt_dir + "/*.txt")

# Combine all text from the .txt files
combined_text = ""
for txt_file in txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
        combined_text += file.read()

# Create the word cloud from the combined text
wordcloud = WordCloud(width=800, height=800, background_color='white').generate(combined_text)

# Display the word cloud using matplotlib
plt.figure(figsize=(8, 8), dpi=80)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Don't show axes for a clean image
plt.show()

# Optionally, you can save the word cloud to an image file
wordcloud.to_file("wordcloud.png")

