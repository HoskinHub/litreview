#code for companion table in lit review (companion to Fig 1)
#keep only the columns with the starter "benefit_"
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('/Users/zoehoskin/Library/CloudStorage/OneDrive-UniversityofToronto/zoes_project/lit_review_cba_iaq/lit_review_data_collection.xlsx')

# Keep all columns in df1 that start with "benefit_" and drop the rest of the columns
df = df.filter(regex='^benefit_')

ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

t = table(ax, df)
t.auto_set_font_size(False)
t.set_fontsize(12)
fig.savefig("test.png")

#sketch out columns you want:
#study citation
#country
#specific location if applicable "benefit_specificlocation"
#population subgroup (urban, asthma, kids, etc. - language convention)
#pollutant
#building type
#intervention type
#scenarios -- HOW?
#study type (language convention)
#health impacts considerered
#performance impacts considered
#costs considered (language convention)
#mortality considered and metric of mortality consideration (language convention)
#original currency
#original value (if not originally percapita)
#year of currency considered for inflation
#time horizon - additional lengths besides annual? Converstion from 10 years??
#findings (results summary)
#note of error bars or error considered
#important notes
#look at how they do this in other lit reviews -- title or not?