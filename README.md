# Hypocognition Analysis

This project explores the relationship between linguistic structures (lemmatized nouns) and psychological/societal data, specifically integrating datasets like Tamir (2016) and Sun(2020) COVID-19 country-level statistics. It featured into [this](https://osf.io/xykvf/overview) project.
## 📁 Project Structure
```Plaintext

.
├── data/
│   ├── external/     # Reference data: Language mappings, stopwords, and selection criteria.
│   ├── processed/    # Output: Merged datasets and statistical results (e.g., tamir_bila_stats).
│   └── raw/          # Input: Original large datasets (e.g., lemmatized nouns, .sav files). You need to put the raw datafile here
├── notebooks/        # Development: Exploratory Data Analysis (EDA) and prototyping. This is really where you start
├── src/              # Source code: Modular Python scripts for the analysis pipeline.
├── reports/figures/  # Visualization: Exported plots and interactive HTML reports.
├── requirements.txt  # Project dependencies.
└── setup_project.py  # Script to initialize directory structure.
```
## 🚀 Getting Started
Markdown

### 🚀 Installation & Setup

#### 1. Clone the Repository
To get a local copy of the project, you need to have python and git. <br>
Once you have that, run the following commands in your terminal:

```bash
git clone [https://github.com/AsherKtech/hypocognition.git](https://github.com/AsherKtech/hypocognition.git)
cd hypocognition
```
#### 2. Set Up the Environment

It is recommended to use a virtual environment to manage dependencies:
```bash

# Create a virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txttall -r requirements.txt
```


#### 3. Data Requirements

Due to file size limits and data privacy, the contents of data/raw/ and data/processed/ are not tracked by Version Control. To run the analysis, you must populate `../data/raw/ `with [`bila_long_noun_lemmatized_full.csv`](https://zenodo.org/records/14928058/preview/large_files.zip?include_deleted=0#tree_item1) and or [`Covid51countries.csv`](https://osf.io/s5puc/files/cemh7) and or `Tamir2016data.sav` (available upon request from the authors)



#### 4. Verify Structure
In case the directory structure doesn't come through, you can try running the setup script to ensure all local directories are correctly initialized:
```bash
python setup_project.py
```
#### 5. 📊 Workflow
* there are two research datasets which were analysed in this project.
    * [`Covid51countries.csv`](https://osf.io/s5puc/files/cemh7): Describe the dataset. 20 emotions from 51 countries
    * `Tamir2016data.sav` (available upon request from the authors) : Describe the dataset. 60 emotions from 8 countries

* corresponding to the Sun Covid data, two things were done:
    * [sun_covid.ipynb](/notebooks/sun_covid.ipynb): 
        * This is a notebook which takes in [`Covid51countries.csv`](https://osf.io/s5puc/files/cemh7)
        * pre-cleans it
        * creates a template for selecting what language is desired for each response country
        * details the process of crafting the statistical final product by merging the selected sun covid data with corresponding lexical ellaboration data from the BILA dataset
        * outputs [covid_bila_merge.csv](data/processed/covid_bila_merge.csv)
        * outputs `corr_covid_bila.csv` which is a corellation table

    * [create_outline_selection.py](src/create_outline_selection.py): 
        * A slimmed down pipeline file which takes in [`Covid51countries.csv`](https://osf.io/s5puc/files/cemh7)
        * pre-cleans it
        * outputs a template for selecting what language is desired for each response country called `selection_in_bila.csv`
        * outputs the pre-cleaned sun covid dataset named `pre_cleaned_Covid51countries.csv`

    * [create_covid_bila_merge.py](src/create_covid_bila_merge.py): 
        * which takes in `pre_cleaned_Covid51countries.csv`
        * and takes in `selection_in_bila.csv`. this is a template which the user has filled out manually, specifying which language is used for each response country
        * crafts the statistical final product by merging the selected sun covid data with corresponding lexical ellaboration data from the BILA dataset
        * outputs [covid_bila_merge.csv](data/processed/covid_bila_merge.csv)
        * outputs `corr_covid_bila.csv` which is a corellation table


    

    * [tamir.ipynb](notebooks/tamir.ipynb): describe what this did
        * outputs `tamir_bila_merge.csv`
        * outputs `tamir_bila_stats.csv`
        * outputs `tamir_bila_corr.csv`

    