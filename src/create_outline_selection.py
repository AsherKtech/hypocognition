# load libraries 
import pandas as pd
import numpy as np
import re
import math
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# get the SUN covid study dataset
Covid51countries = pd.read_csv(Path("~/Projects/hypocognition/data/raw/Covid51countries.csv").expanduser())

# add language names to the df
lang_names = pd.read_csv(Path("~/Projects/hypocognition/data/external/lang_names.csv"))
Covid51countries = Covid51countries.merge(lang_names, left_on="language", right_on="Code", how="left")


# merge croatian, bosnian and serbian
scb = ["Serbian", "Croatian", "Bosnian"]
Covid51countries = Covid51countries.drop(columns=['language'])
Covid51countries.loc[Covid51countries["Language_Name"].isin(scb), "Language_Name"] = "Serbian-Croatian-Bosnian"



# We want to use on only one language of responses for each country
# Further, that language cannot be English

# Calculate the number of responses for each country
country_response_count = pd.DataFrame(Covid51countries[['countryname', 'ISO3']].value_counts())

#collect the languages which people used to respond from each country
languages_per_country = Covid51countries.groupby('countryname')['Language_Name'].value_counts().reset_index(name="count")

# mereg num resposes to languages people used
languages_per_country = languages_per_country.merge(
    country_response_count,
    on="countryname",
    how="left"
)

# Clean up
languages_per_country = languages_per_country.rename(columns={"count_x": "lang_responses", "count_y": "total_responses"})
languages_per_country["percent"] = languages_per_country["lang_responses"] / languages_per_country["total_responses"] * 100



languages_per_country.to_csv(Path("~/Projects/hypocognition/data/processed/languages_per_country.csv").expanduser())


non_eng = languages_per_country[languages_per_country['Language_Name'] != "English"]

# gather list of top names
try:
    del top
except:
    pass
for n in non_eng['countryname'].unique():
    df = non_eng[non_eng['countryname'] == n].reset_index(drop=True)
    try:
        top = pd.concat([top, df.iloc[0:len(df)]], ignore_index=True)
    except:
        top = df.iloc[0:len(df)]


covid_to_bila_nouns_full_lang_name_mapping = pd.read_csv(Path("~/Projects/hypocognition/data/external/covid_to_full_bila_lang_name_mapping.csv"))

# Add the mapping to our selection table
selection = top.merge(
    covid_to_bila_nouns_full_lang_name_mapping,
    left_on="Language_Name",
    right_on = "study_language_names",
    how = "left"
).drop(columns=["code", "study_language_names"])
selection['Selected'] = 0 #np.nan


# simplest way to get the table right is to just tweak it in excel and load it back in. Mark the "Selection" column of outline_selection.csv with 1 for the languages we want to use
selection.to_csv(Path("~/Projects/hypocognition/data/processed/outline_selection.csv").expanduser())

Covid51countries.to_csv(Path("~/Projects/hypocognition/data/processed/pre_cleaned_Covid51countries.csv").expanduser())