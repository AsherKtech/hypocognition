# Hypocognition Analysis

This project explores the relationship between linguistic structures (lemmatized nouns) and psychological/societal data, specifically integrating datasets like Tamir (2016) and COVID-19 country-level statistics.
## 📁 Project Structure
```Plaintext

.
├── data/
│   ├── external/     # Reference data: Language mappings, stopwords, and selection criteria.
│   ├── processed/    # Output: Merged datasets and statistical results (e.g., tamir_bila_stats).
│   └── raw/          # Input: Original large datasets (e.g., lemmatized nouns, .sav files). You need to put the raw datafile here
├── notebooks/        # Development: Exploratory Data Analysis (EDA) and prototyping. This is really where you start
├── src/              # Source code: Modular Python scripts for the analysis pipeline. I haven't made any yet
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

Due to file size limits and data privacy, the contents of data/raw/ and data/processed/ are not tracked by Version Control. To run the analysis, you must populate data/raw/ with [bila_long_noun_lemmatized_full.csv](https://technionmail-my.sharepoint.com/:x:/g/personal/asher_katz_technion_ac_il/IQCvK9cqDUUPS5s6CcaTJw1lAe_LzvDZGefrtEFD4eT7yJA?e=lcykHX) and or [Covid51countries.csv](https://technionmail-my.sharepoint.com/:x:/g/personal/asher_katz_technion_ac_il/IQCDhsIzzuGxQqPQY9n0tpa1AUvXdi6lSeoicGv4w1yYfWc?e=DipX4S) and or [Tamir2016data.sav](https://technionmail-my.sharepoint.com/:u:/g/personal/asher_katz_technion_ac_il/IQC0lW7ejo8USK8xq2AIUNE7AYzzoRz62lc7Vok7G3B_E-k?e=bE7gQ0)



#### 4. Verify Structure
In case the directory structure doesn't come through, you can try running the setup script to ensure all local directories are correctly initialized:
```bash
python setup_project.py
```
#### 5. 📊 Workflow

    Exploration: Use the Jupyter notebooks in notebooks/ to walk through the data merging process. They are a bit of a mess now but If you run the whole thing it will generate the outputs and deposit them into the processed folder.

    Visualization: Summary figures and correlation plots are saved in reports/figures/.