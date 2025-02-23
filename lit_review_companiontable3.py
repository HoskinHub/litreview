import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt

df = pd.read_csv('lit_data.csv', encoding='latin1')

#benefit_net isn't translated for ppp and cpi
table1_df = df[['benefit_citation', 'benefit_country', 'benefit_location', 'benefit_specificlocation', 'benefit_type', 'benefit_pollutant', 'benefit_healthorprod', 'benefit_studytype', 'benefit_net']] #add an elevated_concentration_code column: wildfires, ambient, industrial, none
table1_df = table1_df.rename(columns={
    'benefit_citation': 'citation',
    'benefit_country': 'country',
    'benefit_location': 'building type',
    'benefit_specificlocation': 'specific location',
    'benefit_type': 'intervention',
    'benefit_pollutant': 'pollutant',
    'benefit_healthorprod': 'outcomes',
    'benefit_studytype': 'model or experiment',
    'benefit_net': 'net benefit'
})

table1_df = table1_df.drop_duplicates(subset='citation', keep='first')

# citation, country, location, population subgroup, pollutant, building type, intervention type, scenarios, study type, health impacts, performance impacts, costs, mortality, original currency, original value, year of currency, time horizon, findings, error bars, notes
table2_df = df[['benefit_citation', 'metric', 'benefit_model_inputs_list', 'benefit_mortalityincluded (1=yes)',	'benefit_mortality_details']]

# Rename columns in table2_df
table2_df = table2_df.rename(columns={
    'benefit_citation': 'citation',
    'metric': 'metric',
    'benefit_model_inputs_list': 'model inputs',
    'benefit_mortalityincluded (1=yes)': 'mortality included',
    'benefit_mortality_details': 'mortality details'
})

#table2_df = df['benefit_citation', 'benefit_metric', 'benefit_model_inputs_list', 'benefit_mortalityincluded (1=yes)',	'benefit_mortality_details']]

table1_df.to_csv('table1_df.csv', index=False)
table2_df.to_csv('table2_df.csv', index=False)

#fig, ax = plt.subplots(figsize=(12, 8)) 

#tbl1 = table(ax, table1_df, loc='center', cellLoc='center')
#plt.savefig("table1_df.png", bbox_inches='tight')

#tbl2 = table(ax, table2_df, loc='center', cellLoc='center')
#plt.savefig("table2_df.png", bbox_inches='tight')
#elevated concentration

#unique



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