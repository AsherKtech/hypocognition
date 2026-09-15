#%%
# load libraries 
import pandas as pd
import numpy as np
import re
import math
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

#%%
# get the SUN covid study dataset
Covid51countries = pd.read_csv(Path("~/Projects/hypocognition/data/processed/pre_cleaned_Covid51countries.csv").expanduser())

#%%
# Rename outline_selection.csv to selection_in_bila.csv and load it back in.
selection = pd.read_csv(Path("~/Projects/hypocognition/data/processed/selection_in_bila.csv").expanduser(), index_col=0).reset_index(drop=True)
selection = selection[selection['Selected']==1].rename(columns={'study_language_names':"Language_Name"} )

#%%
# Lets try filtering the dataset using our new selection
filtered = Covid51countries.merge(
    selection,
    on=['countryname', 'Language_Name'],
    how='inner'
)

filtered.to_csv(Path("~/Projects/hypocognition/data/processed/selection_in_covid.csv").expanduser())


#%%
emotions = ['admiration', 'calm', 'compassion',
       'determination', 'moved', 'gratitude', 'hope', 'love', 'relief',
       'pleasure', 'anger', 'anxiety', 'boredom', 'confusion', 'disgust',
       'fear', 'frustration', 'loneliness', 'regret', 'sadness']

# select only the columns we need for the analysis
filtered=filtered[['country', 'countryname', 'Language_Name', 'lang_responses',
       'total_responses', 'percent', 'bila_language_name_mapping',
       'possible_alternative_bila_language_name_mappings', 'Selected','ISO3', 'admiration', 'calm', 'compassion',
       'determination', 'moved', 'gratitude', 'hope', 'love', 'relief',
       'pleasure', 'anger', 'anxiety', 'boredom', 'confusion', 'disgust',
       'fear', 'frustration', 'loneliness', 'regret', 'sadness']]


#%%
# get the dataset of the dictionaries. We will look at how elaborated each of the twenty emotions are in each of the 39 languages
bila_nouns_full = pd.read_csv(Path("~/Projects/hypocognition/data/raw/bila_long_noun_lemmatized_full.csv").expanduser(), index_col=0)


#%%
# remove stopwords as per the original bila authors
with open(Path("~/Projects/hypocognition/data/external/stopwords.txt").expanduser()) as f:
    words = [line.strip() for line in f if line.strip()]
    
bila_nouns_full = bila_nouns_full[~bila_nouns_full["word"].isin(words)]


tot_words = bila_nouns_full.groupby('id')['word'].nunique().reset_index(name='Total_words_in_dict')
tot_counts = bila_nouns_full.groupby('id')['count'].sum().reset_index(name='Total_counts_in_dict')


#%%



#%%
# I think we will needs these later
dictionary_means = (
    bila_nouns_full
        .groupby('id', as_index=False)['count']
        .mean()
        .rename(columns={'count': 'dictionary_count_mean'})
)

# filter just the emotions
bila_nouns_full_emotions = bila_nouns_full[bila_nouns_full['word'].isin(emotions)].reset_index(drop=True)


# already filtered out everything but the 18 emotions
# now we want to filter evrything but the 29 dictionaries
# Where are lang_name and Language_Names the Same?
bila_nouns_full_emotions_filtered = bila_nouns_full_emotions[bila_nouns_full_emotions['langname'].isin(filtered['bila_language_name_mapping'].unique())].reset_index(drop=True)

filtered = filtered.loc[:, ~filtered.columns.duplicated()]

#%%
word_counts = (
    bila_nouns_full_emotions_filtered
    .groupby("langname")["word"]
    .nunique()
    .reset_index(name="n_unique_words")
)


#%%
# add the rows of the emotions words which don't appear in each dictionary

full_index = pd.MultiIndex.from_product(
    [bila_nouns_full_emotions_filtered["id"].unique(), bila_nouns_full_emotions_filtered["word"].unique()],
    names=["id", "word"]
)

# use the full index to add the missing values
bila_nouns_full_emotions_filtered_full = (
    bila_nouns_full_emotions_filtered
    .set_index(["id", "word"])
    .reindex(full_index)
    .reset_index()
)
num_cols = ["nsenses", "count", "log_count", 'regression_elaboration', 'dictsize_data', 'simple_elaboration']

#%%
#set the number columns to 0 where NaN
bila_nouns_full_emotions_filtered_full[num_cols] = bila_nouns_full_emotions_filtered_full[num_cols].fillna(0)
meta_cols = [
    "langname", "glottocode", "year", "title", "imprint", "author",
    "area", "langfamily", "affiliation", "longitude", "latitude"
]

# fill the those zero rows with dictionary meta -data
bila_nouns_full_emotions_filtered_full[meta_cols] = (
    bila_nouns_full_emotions_filtered_full
    .groupby("id")[meta_cols]
    .transform("first")
)

#%%
# now we're don emaking datasets, this is a table of just the stuff we need for correlations
elab_per_emotion = bila_nouns_full_emotions_filtered_full[['langname',   'glottocode','word', 'count',  'id', 'year',"simple_elaboration", "regression_elaboration",	"dictsize_data"	]]

#%%
# Make table of the 18 languages for each country
stats_by_country = (
    filtered
    .groupby(['countryname', 'bila_language_name_mapping'])[emotions]
    .agg(['mean', 'std'])
)
stats_by_country = pd.DataFrame(stats_by_country)


# lets just flatten out the 3 level column names
stats_by_country.columns = [
    f"{emotion}_{stat}" for emotion, stat in stats_by_country.columns
]
stats_by_country = stats_by_country.reset_index()

#%%
# it was very wide, lets make it narrow, longer, and more robust
stats_long = (
    stats_by_country
    .set_index(['countryname', 'bila_language_name_mapping'])
    .filter(regex='_(mean|std)$')
    .stack()
    .reset_index()
)

stats_long[['word', 'stat']] = stats_long['level_2'].str.rsplit('_', n=1, expand=True)
stats_long = stats_long.rename(columns={0: 'value'}).drop(columns='level_2')

#%%
stats_long = (
    stats_long
    .pivot_table(
        index=['countryname', 'bila_language_name_mapping', 'word'],
        columns='stat',
        values='value'
    )
    .reset_index()
)

#%%
#Merge our cleaned survey data with the BILA dictionary data
merged = elab_per_emotion.merge(
    stats_long,
    left_on=['langname', 'word'],
    right_on=['bila_language_name_mapping', 'word'],
    how='left'
)

# add the dictionary_count_mean column
merged = merged.merge(
    dictionary_means,
    left_on='id',
    right_on='id',
    how='left'
)


#%%
merged = merged[merged['countryname'].notna()]

# clarify the meaning of mean
merged = merged.rename(columns={'mean': "response_mean"})
# Clarify what std we're talking about
merged = merged.rename(columns={'std': "response_std"})
# drop a bunch of columns

merged = merged[['langname', 'glottocode', 'word', 'count', 'id', 'year',
       'simple_elaboration', 'regression_elaboration', 'dictsize_data',
       'countryname', 'bila_language_name_mapping', 'response_mean',
       'response_std', 'dictionary_count_mean' ]]
merged = merged.sort_values(by=["langname", 'word'])

merged = merged.reset_index(drop=True)

merged = merged.sort_values(by=["langname", 'countryname','word'])
merged = merged.reset_index(drop=True)
merged = merged.fillna(0)

#%%
merged.to_csv(Path("~/Projects/hypocognition/data/processed/covid_bila_merge.csv").expanduser())



#%%
merged2 = merged.copy()

# log count
merged2["log_count"] = np.log(merged2["count"] + 1)

# absolute distance from midpoint
SCALE_MIDPOINT = merged2["response_mean"].mean()
merged2["abs_dist_midpoint"] = (
    merged2["response_mean"] - SCALE_MIDPOINT
).abs()


#%%
result = (
    merged2
    .groupby(["countryname", "langname", "id"])
    .agg(
        corr_logcount_response_mean=(
            "log_count",
            lambda x: x.corr(
                merged2.loc[x.index, "response_mean"]
            )
        ),
        corr_logcount_response_sd=(
            "log_count",
            lambda x: x.corr(
                merged2.loc[x.index, "response_std"]
            )
        ),
        corr_logcount_abs_dist_midpoint=(
            "log_count",
            lambda x: x.corr(
                merged2.loc[x.index, "abs_dist_midpoint"]
            )
        ),

    )
    .reset_index()
)
#%%
result.to_csv(Path("~/Projects/hypocognition/data/processed/corr_covid_bila.csv").expanduser())